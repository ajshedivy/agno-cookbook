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
    parser.add_argument("--agent-id", help="Agent ID to run (default: first available)")
    parser.add_argument("--message", "-m", help="Message to send to the agent")
    parser.add_argument("--stream", "-s", action="store_true", help="Stream the response")
    parser.add_argument("--session-id", help="Session ID for persistent conversations")
    parser.add_argument("--user-id", help="User ID for user-specific memory")
    parser.add_argument("--dependencies", help="JSON string of dependencies to pass to agent tools")
    args = parser.parse_args()

    client = AgentOSClient(base_url=args.base_url)

    if args.message:
        await run_agent(client, args.agent_id, args.message, args.stream, args.session_id, args.user_id, args.dependencies)
    else:
        await list_agents(client)


if __name__ == "__main__":
    asyncio.run(main())
