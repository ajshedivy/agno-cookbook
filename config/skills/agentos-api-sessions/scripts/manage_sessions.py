#!/usr/bin/env python3
"""
Query and manage sessions on an AgentOS instance.

Examples:
    # List all sessions
    python manage_sessions.py

    # List sessions for a specific agent
    python manage_sessions.py --agent-id researcher

    # List sessions for a specific user
    python manage_sessions.py --user-id alice@example.com

    # Show runs inside a specific session
    python manage_sessions.py --session-id abc-123 --show-runs

    # Create a new session
    python manage_sessions.py --create --agent-id my-agent --user-id alice --name "Research Chat"

    # Rename a session
    python manage_sessions.py --session-id abc-123 --rename "New Name"

    # Delete a session
    python manage_sessions.py --session-id abc-123 --delete

    # Use a different server
    python manage_sessions.py --base-url http://my-server:8000
"""

import argparse
import asyncio
import sys

from agno.client import AgentOSClient


async def list_sessions(
    client: AgentOSClient,
    agent_id: str | None,
    user_id: str | None,
    limit: int,
) -> None:
    kwargs: dict = {"limit": limit}
    if agent_id:
        kwargs["component_id"] = agent_id
    if user_id:
        kwargs["user_id"] = user_id

    sessions = await client.get_sessions(**kwargs)
    if not sessions.data:
        print("No sessions found")
        return

    print(f"Found {len(sessions.data)} session(s):\n")
    for sess in sessions.data:
        name = sess.session_name or "Unnamed"
        created = getattr(sess, "created_at", "")
        print(f"  {sess.session_id}")
        print(f"    name: {name}")
        if created:
            print(f"    created: {created}")
        print()


async def show_session_runs(client: AgentOSClient, session_id: str) -> None:
    runs = await client.get_session_runs(session_id=session_id)
    if not runs:
        print(f"No runs found for session {session_id}")
        return

    print(f"Session {session_id} — {len(runs)} run(s):\n")
    for run in runs:
        content = str(run.content or "")
        preview = (content[:120] + "...") if len(content) > 120 else content
        print(f"  [{run.run_id}]")
        print(f"    {preview}")
        print()


async def create_session(
    client: AgentOSClient,
    agent_id: str,
    user_id: str | None,
    name: str | None,
) -> None:
    kwargs: dict = {"agent_id": agent_id}
    if user_id:
        kwargs["user_id"] = user_id
    if name:
        kwargs["session_name"] = name

    session = await client.create_session(**kwargs)
    print(f"Created session: {session.session_id}")
    if session.session_name:
        print(f"  name: {session.session_name}")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Manage sessions via AgentOS API")
    parser.add_argument("--base-url", default="http://localhost:7777", help="AgentOS server URL (default: http://localhost:7777)")
    parser.add_argument("--session-id", help="Session ID to inspect, rename, or delete")
    parser.add_argument("--agent-id", help="Filter sessions by agent ID")
    parser.add_argument("--user-id", help="Filter sessions by user ID")
    parser.add_argument("--limit", type=int, default=20, help="Max sessions to list (default: 20)")
    parser.add_argument("--show-runs", action="store_true", help="Show runs for the given --session-id")
    parser.add_argument("--create", action="store_true", help="Create a new session (requires --agent-id)")
    parser.add_argument("--rename", metavar="NAME", help="Rename the session (requires --session-id)")
    parser.add_argument("--name", help="Session name (for --create)")
    parser.add_argument("--delete", action="store_true", help="Delete the session (requires --session-id)")
    args = parser.parse_args()

    client = AgentOSClient(base_url=args.base_url)

    if args.create:
        if not args.agent_id:
            print("--create requires --agent-id", file=sys.stderr)
            sys.exit(1)
        await create_session(client, args.agent_id, args.user_id, args.name)
    elif args.delete:
        if not args.session_id:
            print("--delete requires --session-id", file=sys.stderr)
            sys.exit(1)
        await client.delete_session(args.session_id)
        print(f"Deleted session: {args.session_id}")
    elif args.rename:
        if not args.session_id:
            print("--rename requires --session-id", file=sys.stderr)
            sys.exit(1)
        renamed = await client.rename_session(session_id=args.session_id, session_name=args.rename)
        print(f"Renamed session {args.session_id} to: {renamed.session_name}")
    elif args.session_id and args.show_runs:
        await show_session_runs(client, args.session_id)
    elif args.session_id:
        details = await client.get_session(args.session_id)
        print(f"Session: {details.session_id}")
        print(f"  name: {getattr(details, 'session_name', 'N/A')}")
        print(f"  agent: {getattr(details, 'agent_id', 'N/A')}")
        print(f"  user: {getattr(details, 'user_id', 'N/A')}")
        print(f"  state: {getattr(details, 'session_state', {})}")
    else:
        await list_sessions(client, args.agent_id, args.user_id, args.limit)


if __name__ == "__main__":
    asyncio.run(main())
