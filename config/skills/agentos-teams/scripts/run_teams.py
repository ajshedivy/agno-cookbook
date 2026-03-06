"""
Run teams via AgentOSClient — streaming and non-streaming.

Prerequisites:
1. Start an AgentOS server with teams configured
2. Run this script: python run_teams.py
"""

import asyncio

from agno.client import AgentOSClient
from agno.run.team import RunCompletedEvent, RunContentEvent


async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    if not config.teams:
        print("No teams available")
        return

    team_id = config.teams[0].id
    print(f"Using team: {team_id}")

    # Non-streaming run
    print("\n--- Non-Streaming ---")
    result = await client.run_team(
        team_id=team_id,
        message="What is the capital of France and what is 15 * 7?",
    )
    print(f"Run ID: {result.run_id}")
    print(f"Content: {result.content}")

    # Streaming run
    print("\n--- Streaming ---")
    async for event in client.run_team_stream(
        team_id=team_id,
        message="Compare Python and Rust.",
    ):
        if isinstance(event, RunContentEvent):
            print(event.content, end="", flush=True)
        elif isinstance(event, RunCompletedEvent):
            print(f"\nDone! Run ID: {event.run_id}")


if __name__ == "__main__":
    asyncio.run(main())
