#!/usr/bin/env python3
"""
Discover and run teams on an AgentOS instance.

Examples:
    # List all available teams
    python run_teams.py

    # Run a specific team with a message
    python run_teams.py --team-id research-team --message "Compare Python and Rust"

    # Stream a response from the first available team
    python run_teams.py --message "Analyze Tesla stock" --stream

    # Run against a remote server
    python run_teams.py --base-url http://my-server:8000 --message "Research AI trends"

    # Multi-turn team conversation
    python run_teams.py --message "Analyze NVIDIA" --session-id research-1
    python run_teams.py --message "Now compare to AMD" --session-id research-1
"""

import argparse
import asyncio
import sys

from agno.client import AgentOSClient
from agno.run.team import RunCompletedEvent, RunContentEvent


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
    parser.add_argument("--team-id", help="Team ID to run (default: first available)")
    parser.add_argument("--message", "-m", help="Message to send to the team")
    parser.add_argument("--stream", "-s", action="store_true", help="Stream the response")
    parser.add_argument("--session-id", help="Session ID for persistent conversations")
    parser.add_argument("--user-id", help="User ID")
    args = parser.parse_args()

    client = AgentOSClient(base_url=args.base_url)

    if args.message:
        await run_team(client, args.team_id, args.message, args.stream, args.session_id, args.user_id)
    else:
        await list_teams(client)


if __name__ == "__main__":
    asyncio.run(main())
