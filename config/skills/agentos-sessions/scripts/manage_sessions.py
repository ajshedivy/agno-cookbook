"""
Session management via AgentOSClient.

Prerequisites:
1. Start an AgentOS server with storage configured
2. Run this script: python manage_sessions.py
"""

import asyncio

from agno.client import AgentOSClient


async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    if not config.agents:
        print("No agents available")
        return

    agent_id = config.agents[0].id
    user_id = "example-user"

    # Create a session
    print("1. Creating session...")
    session = await client.create_session(
        agent_id=agent_id,
        user_id=user_id,
        session_name="Demo Session",
    )
    print(f"   Session ID: {session.session_id}")

    # List sessions
    print("\n2. Listing sessions...")
    sessions = await client.get_sessions(user_id=user_id)
    for sess in sessions.data[:5]:
        print(f"   {sess.session_id}: {sess.session_name or 'Unnamed'}")

    # Run messages in session
    print("\n3. Running messages...")
    await client.run_agent(
        agent_id=agent_id,
        message="My name is Alice.",
        session_id=session.session_id,
    )
    result = await client.run_agent(
        agent_id=agent_id,
        message="What's my name?",
        session_id=session.session_id,
    )
    print(f"   Response: {result.content}")

    # Get session runs
    print("\n4. Getting session runs...")
    runs = await client.get_session_runs(session_id=session.session_id)
    print(f"   Found {len(runs)} runs")

    # Rename and delete
    print("\n5. Renaming session...")
    renamed = await client.rename_session(
        session_id=session.session_id,
        session_name="Renamed Session",
    )
    print(f"   New name: {renamed.session_name}")

    print("\n6. Deleting session...")
    await client.delete_session(session.session_id)
    print("   Done")


if __name__ == "__main__":
    asyncio.run(main())
