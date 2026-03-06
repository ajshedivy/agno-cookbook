"""
Run agents via AgentOSClient — streaming and non-streaming.

Prerequisites:
1. Start an AgentOS server: python start_agentos.py
2. Run this script: python run_agents.py
"""

import asyncio

from agno.client import AgentOSClient
from agno.run.agent import RunCompletedEvent, RunContentEvent


async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    # Discover agents
    config = await client.aget_config()
    if not config.agents:
        print("No agents available")
        return

    agent_id = config.agents[0].id
    print(f"Using agent: {agent_id}")

    # Non-streaming run
    print("\n--- Non-Streaming ---")
    result = await client.run_agent(
        agent_id=agent_id,
        message="What is 2 + 2?",
    )
    print(f"Run ID: {result.run_id}")
    print(f"Content: {result.content}")

    # Streaming run
    print("\n--- Streaming ---")
    async for event in client.run_agent_stream(
        agent_id=agent_id,
        message="Tell me a short joke.",
    ):
        if isinstance(event, RunContentEvent):
            print(event.content, end="", flush=True)
        elif isinstance(event, RunCompletedEvent):
            print(f"\nDone! Run ID: {event.run_id}")


if __name__ == "__main__":
    asyncio.run(main())
