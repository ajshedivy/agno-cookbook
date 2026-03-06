#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["agno[os]"]
# ///
"""
Discover and run agents on an AgentOS instance.

Examples:
    # List all available agents
    uv run run_agents.py

    # Show full AgentOS config (agents, teams, workflows, databases, etc.)
    uv run run_agents.py --config

    # Show detailed config for a specific agent (tools, model, knowledge, memory)
    uv run run_agents.py --config --agent-id my-agent

    # Run a specific agent with a message
    uv run run_agents.py --agent-id my-agent --message "What is 2 + 2?"

    # Stream a response from the first available agent
    uv run run_agents.py --message "Tell me a joke" --stream

    # Run against a remote server
    uv run run_agents.py --base-url http://my-server:8000 --message "Hello"

    # Run with session persistence
    uv run run_agents.py --agent-id my-agent --message "My name is Alice" --session-id chat-1
    uv run run_agents.py --agent-id my-agent --message "What is my name?" --session-id chat-1

    # Pass dependencies to agent tools
    uv run run_agents.py --message "Greet me" --dependencies '{"robot_name": "Anna"}'
"""

import argparse
import asyncio
import json
import sys

from agno.client import AgentOSClient
from agno.run.agent import RunCompletedEvent, RunContentEvent


async def show_config(client: AgentOSClient, agent_id: str | None) -> None:
    if agent_id:
        agent = await client.aget_agent(agent_id)
        print(f"Agent: {agent.id}")
        print(f"  name: {agent.name}")
        if agent.model:
            print(f"  model: {agent.model}")
        if agent.description:
            print(f"  description: {agent.description}")

        # Tools
        tools_dict = agent.tools or {}
        for _, tool_list in tools_dict.items():
            print(f"\n  tools ({len(tool_list)}):")
            for t in tool_list:
                name = t.get("name", "unknown")
                desc = t.get("description", "")
                preview = desc[:100].replace("\n", " ")
                if len(desc) > 100:
                    preview += "..."
                print(f"    - {name}: {preview}")

        # Knowledge
        if agent.knowledge:
            print(f"\n  knowledge: {agent.knowledge}")

        # Memory
        if agent.memory:
            print(f"\n  memory: {agent.memory}")
        return

    config = await client.aget_config()
    print(f"AgentOS ID: {config.os_id}")
    if config.name:
        print(f"Name: {config.name}")
    print(f"Databases: {', '.join(config.databases or [])}")

    # Agents
    agents = config.agents or []
    print(f"\nAgents ({len(agents)}):")
    for a in agents:
        print(f"  - {a.id}: {a.name}")

    # Teams
    teams = config.teams or []
    if teams:
        print(f"\nTeams ({len(teams)}):")
        for t in teams:
            mode = f" (mode: {t.mode})" if t.mode else ""
            print(f"  - {t.id}: {t.name}{mode}")

    # Workflows
    workflows = config.workflows or []
    if workflows:
        print(f"\nWorkflows ({len(workflows)}):")
        for w in workflows:
            print(f"  - {w.id}: {w.name}")

    # Knowledge
    if config.knowledge and config.knowledge.knowledge_instances:
        instances = config.knowledge.knowledge_instances
        print(f"\nKnowledge ({len(instances)}):")
        for k in instances:
            print(f"  - {k.name} (table: {k.table}, db: {k.db_id})")

    # Chat quick prompts
    if config.chat and config.chat.quick_prompts:
        print(f"\nQuick Prompts:")
        for agent_id, prompts in config.chat.quick_prompts.items():
            print(f"  {agent_id}:")
            for p in prompts:
                print(f"    - {p}")


async def list_agents(client: AgentOSClient) -> None:
    config = await client.aget_config()
    agents = config.agents or []
    if not agents:
        print("No agents available")
        return

    print(f"Found {len(agents)} agent(s):\n")
    for agent in agents:
        detail = await client.aget_agent(agent.id)
        model_info = f" | model: {detail.model}" if detail.model else ""
        tools_count = len(detail.tools or [])
        print(f"  {agent.id}")
        print(f"    name: {detail.name}{model_info}")
        print(f"    tools: {tools_count}")
        if detail.description:
            print(f"    description: {detail.description}")
        print()


async def run_agent(
    client: AgentOSClient,
    agent_id: str | None,
    message: str,
    stream: bool,
    session_id: str | None,
    user_id: str | None,
    dependencies: str | None,
) -> None:
    if not agent_id:
        config = await client.aget_config()
        if not config.agents:
            print("No agents available", file=sys.stderr)
            sys.exit(1)
        agent_id = config.agents[0].id
        print(f"Using agent: {agent_id}\n")

    run_kwargs: dict = {
        "agent_id": agent_id,
        "message": message,
    }
    if session_id:
        run_kwargs["session_id"] = session_id
    if user_id:
        run_kwargs["user_id"] = user_id
    if dependencies:
        run_kwargs["dependencies"] = json.loads(dependencies)

    if stream:
        async for event in client.run_agent_stream(**run_kwargs):
            if isinstance(event, RunContentEvent):
                print(event.content, end="", flush=True)
            elif isinstance(event, RunCompletedEvent):
                print(f"\n\n[run_id: {event.run_id}]")
    else:
        result = await client.run_agent(**run_kwargs)
        print(result.content)
        print(f"\n[run_id: {result.run_id}]")
        if result.metrics:
            print(f"[tokens: {result.metrics.total_tokens}]")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run agents via AgentOS API")
    parser.add_argument("--base-url", default="http://localhost:7777", help="AgentOS server URL (default: http://localhost:7777)")
    parser.add_argument("--config", "-c", action="store_true", help="Show AgentOS config (combine with --agent-id for agent-specific config)")
    parser.add_argument("--agent-id", help="Agent ID to run (default: first available)")
    parser.add_argument("--message", "-m", help="Message to send to the agent")
    parser.add_argument("--stream", "-s", action="store_true", help="Stream the response")
    parser.add_argument("--session-id", help="Session ID for persistent conversations")
    parser.add_argument("--user-id", help="User ID for user-specific memory")
    parser.add_argument("--dependencies", help="JSON string of dependencies to pass to agent tools")
    args = parser.parse_args()

    client = AgentOSClient(base_url=args.base_url)

    if args.config:
        await show_config(client, args.agent_id)
    elif args.message:
        await run_agent(client, args.agent_id, args.message, args.stream, args.session_id, args.user_id, args.dependencies)
    else:
        await list_agents(client)


if __name__ == "__main__":
    asyncio.run(main())
