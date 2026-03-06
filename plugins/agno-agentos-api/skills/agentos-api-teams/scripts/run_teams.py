#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["agno[os]"]
# ///
"""
Discover and run teams on an AgentOS instance.

Examples:
    # List all available teams
    uv run run_teams.py

    # Show full AgentOS config (teams, agents, workflows, databases)
    uv run run_teams.py --config

    # Show detailed config for a specific team (members, model, tools)
    uv run run_teams.py --config --team-id my-team

    # Run a specific team with a message
    uv run run_teams.py --team-id research-team --message "Compare Python and Rust"

    # Stream a response from the first available team
    uv run run_teams.py --message "Analyze Tesla stock" --stream

    # Run against a remote server
    uv run run_teams.py --base-url http://my-server:8000 --message "Research AI trends"

    # Multi-turn team conversation
    uv run run_teams.py --message "Analyze NVIDIA" --session-id research-1
    uv run run_teams.py --message "Now compare to AMD" --session-id research-1
"""

import argparse
import asyncio
import sys

from agno.client import AgentOSClient
from agno.run.team import RunCompletedEvent, RunContentEvent


async def show_config(client: AgentOSClient, team_id: str | None) -> None:
    if team_id:
        team = await client.aget_team(team_id)
        print(f"Team: {team.id}")
        print(f"  name: {team.name}")
        if team.mode:
            print(f"  mode: {team.mode}")
        if team.model:
            print(f"  model: {team.model}")
        if team.description:
            print(f"  description: {team.description}")

        members = team.members or []
        print(f"\n  members ({len(members)}):")
        for m in members:
            tools_count = sum(len(tl) for tl in (m.tools or {}).values())
            print(f"    - {m.id}: {m.name}")
            if m.model:
                print(f"        model: {m.model}")
            print(f"        tools: {tools_count}")
            if m.description:
                preview = m.description[:120].replace("\n", " ")
                if len(m.description) > 120:
                    preview += "..."
                print(f"        description: {preview}")

        if team.knowledge:
            print(f"\n  knowledge: {team.knowledge}")
        if team.memory:
            print(f"\n  memory: {team.memory}")
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
    print(f"\nTeams ({len(teams)}):")
    for t in teams:
        mode = f" (mode: {t.mode})" if t.mode else ""
        print(f"  - {t.id}: {t.name}{mode}")

    workflows = config.workflows or []
    if workflows:
        print(f"\nWorkflows ({len(workflows)}):")
        for w in workflows:
            print(f"  - {w.id}: {w.name}")


async def list_teams(client: AgentOSClient) -> None:
    config = await client.aget_config()
    teams = config.teams or []
    if not teams:
        print("No teams available")
        return

    print(f"Found {len(teams)} team(s):\n")
    for team in teams:
        print(f"  {team.id}")
        if hasattr(team, "name") and team.name:
            print(f"    name: {team.name}")
        if hasattr(team, "description") and team.description:
            print(f"    description: {team.description}")
        print()


async def run_team(
    client: AgentOSClient,
    team_id: str | None,
    message: str,
    stream: bool,
    session_id: str | None,
    user_id: str | None,
) -> None:
    if not team_id:
        config = await client.aget_config()
        if not config.teams:
            print("No teams available", file=sys.stderr)
            sys.exit(1)
        team_id = config.teams[0].id
        print(f"Using team: {team_id}\n")

    run_kwargs: dict = {"team_id": team_id, "message": message}
    if session_id:
        run_kwargs["session_id"] = session_id
    if user_id:
        run_kwargs["user_id"] = user_id

    if stream:
        async for event in client.run_team_stream(**run_kwargs):
            if isinstance(event, RunContentEvent):
                print(event.content, end="", flush=True)
            elif isinstance(event, RunCompletedEvent):
                print(f"\n\n[run_id: {event.run_id}]")
    else:
        result = await client.run_team(**run_kwargs)
        print(result.content)
        print(f"\n[run_id: {result.run_id}]")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run teams via AgentOS API")
    parser.add_argument("--base-url", default="http://localhost:7777", help="AgentOS server URL (default: http://localhost:7777)")
    parser.add_argument("--config", "-c", action="store_true", help="Show AgentOS config (combine with --team-id for team-specific config)")
    parser.add_argument("--team-id", help="Team ID to run (default: first available)")
    parser.add_argument("--message", "-m", help="Message to send to the team")
    parser.add_argument("--stream", "-s", action="store_true", help="Stream the response")
    parser.add_argument("--session-id", help="Session ID for persistent conversations")
    parser.add_argument("--user-id", help="User ID")
    args = parser.parse_args()

    client = AgentOSClient(base_url=args.base_url)

    if args.config:
        await show_config(client, args.team_id)
    elif args.message:
        await run_team(client, args.team_id, args.message, args.stream, args.session_id, args.user_id)
    else:
        await list_teams(client)


if __name__ == "__main__":
    asyncio.run(main())
