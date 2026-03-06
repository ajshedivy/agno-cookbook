#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["agno[os]"]
# ///
"""
Discover and run workflows on an AgentOS instance.

Examples:
    # List all available workflows
    uv run run_workflows.py

    # Show full AgentOS config (workflows, agents, teams, databases)
    uv run run_workflows.py --config

    # Show detailed config for a specific workflow (steps, agents, tools)
    uv run run_workflows.py --config --workflow-id my-workflow

    # Run a specific workflow
    uv run run_workflows.py --workflow-id qa-workflow --message "Explain machine learning"

    # Stream a workflow response
    uv run run_workflows.py --message "Analyze AI trends" --stream

    # Run against a remote server
    uv run run_workflows.py --base-url http://my-server:8000 --message "Process this"
"""

import argparse
import asyncio
import sys

from agno.client import AgentOSClient


def _print_agent_summary(agent: dict, indent: str = "      ") -> None:
    """Print a summary of an agent dict from a workflow step."""
    name = agent.get("name", "unknown")
    model = agent.get("model")
    tools_dict = agent.get("tools") or {}
    tools_count = sum(len(tl) for tl in tools_dict.values()) if isinstance(tools_dict, dict) else 0
    print(f"{indent}agent: {name}")
    if model:
        print(f"{indent}  model: {model}")
    print(f"{indent}  tools: {tools_count}")


async def show_config(client: AgentOSClient, workflow_id: str | None) -> None:
    if workflow_id:
        wf = await client.aget_workflow(workflow_id)
        print(f"Workflow: {wf.id}")
        print(f"  name: {wf.name}")
        if wf.description:
            print(f"  description: {wf.description}")
        print(f"  db_id: {wf.db_id}")
        if wf.is_component:
            print(f"  is_component: {wf.is_component}")

        data = wf.model_dump()
        steps = data.get("steps") or []
        if steps:
            print(f"\n  steps ({len(steps)}):")
            for i, step in enumerate(steps, 1):
                step_name = step.get("name", f"Step {i}")
                step_type = step.get("type", "")
                print(f"    {i}. {step_name} ({step_type})")
                agent = step.get("agent")
                if agent:
                    _print_agent_summary(agent)
                team = step.get("team")
                if team:
                    team_name = team.get("name", "unknown")
                    members = team.get("members") or []
                    print(f"      team: {team_name} ({len(members)} members)")
                    for m in members:
                        m_tools = sum(len(tl) for tl in (m.get("tools") or {}).values()) if isinstance(m.get("tools"), dict) else 0
                        print(f"        - {m.get('name', 'unknown')}: tools={m_tools}")
        return

    config = await client.aget_config()
    print(f"AgentOS ID: {config.os_id}")
    if config.name:
        print(f"Name: {config.name}")
    print(f"Databases: {', '.join(config.databases or [])}")

    agents = config.agents or []
    if agents:
        print(f"\nAgents ({len(agents)}):")
        for a in agents:
            print(f"  - {a.id}: {a.name}")

    teams = config.teams or []
    if teams:
        print(f"\nTeams ({len(teams)}):")
        for t in teams:
            mode = f" (mode: {t.mode})" if t.mode else ""
            print(f"  - {t.id}: {t.name}{mode}")

    workflows = config.workflows or []
    print(f"\nWorkflows ({len(workflows)}):")
    for w in workflows:
        print(f"  - {w.id}: {w.name}")


async def list_workflows(client: AgentOSClient) -> None:
    config = await client.aget_config()
    workflows = config.workflows or []
    if not workflows:
        print("No workflows available")
        return

    print(f"Found {len(workflows)} workflow(s):\n")
    for wf in workflows:
        print(f"  {wf.id}")
        if hasattr(wf, "name") and wf.name:
            print(f"    name: {wf.name}")
        if hasattr(wf, "description") and wf.description:
            print(f"    description: {wf.description}")
        print()


async def run_workflow(
    client: AgentOSClient,
    workflow_id: str | None,
    message: str,
    stream: bool,
) -> None:
    if not workflow_id:
        config = await client.aget_config()
        if not config.workflows:
            print("No workflows available", file=sys.stderr)
            sys.exit(1)
        workflow_id = config.workflows[0].id
        print(f"Using workflow: {workflow_id}\n")

    if stream:
        async for event in client.run_workflow_stream(
            workflow_id=workflow_id,
            message=message,
        ):
            if event.event == "RunContent" and hasattr(event, "content"):
                print(event.content, end="", flush=True)
            elif event.event == "WorkflowAgentCompleted" and hasattr(event, "content") and event.content:
                print(event.content, end="", flush=True)
        print()
    else:
        result = await client.run_workflow(
            workflow_id=workflow_id,
            message=message,
        )
        print(result.content)
        print(f"\n[run_id: {result.run_id}]")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run workflows via AgentOS API")
    parser.add_argument("--base-url", default="http://localhost:7777", help="AgentOS server URL (default: http://localhost:7777)")
    parser.add_argument("--config", "-c", action="store_true", help="Show AgentOS config (combine with --workflow-id for workflow-specific config)")
    parser.add_argument("--workflow-id", help="Workflow ID to run (default: first available)")
    parser.add_argument("--message", "-m", help="Message to send to the workflow")
    parser.add_argument("--stream", "-s", action="store_true", help="Stream the response")
    args = parser.parse_args()

    client = AgentOSClient(base_url=args.base_url)

    if args.config:
        await show_config(client, args.workflow_id)
    elif args.message:
        await run_workflow(client, args.workflow_id, args.message, args.stream)
    else:
        await list_workflows(client)


if __name__ == "__main__":
    asyncio.run(main())
