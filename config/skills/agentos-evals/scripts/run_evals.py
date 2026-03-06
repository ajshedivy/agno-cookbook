"""
Run evaluations via AgentOSClient.

Prerequisites:
1. Start an AgentOS server with agents
2. Run this script: python run_evals.py
"""

import asyncio

from agno.client import AgentOSClient
from agno.db.schemas.evals import EvalType


async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    if not config.agents:
        print("No agents available")
        return

    agent_id = config.agents[0].id

    # Accuracy eval
    print("1. Running accuracy eval...")
    try:
        result = await client.run_eval(
            agent_id=agent_id,
            eval_type=EvalType.ACCURACY,
            input_text="What is 2 + 2?",
            expected_output="4",
        )
        if result:
            print(f"   Eval ID: {result.id}")
            print(f"   Data: {result.eval_data}")
    except Exception as e:
        print(f"   Error: {e}")

    # Performance eval
    print("\n2. Running performance eval...")
    try:
        result = await client.run_eval(
            agent_id=agent_id,
            eval_type=EvalType.PERFORMANCE,
            input_text="Hello",
            num_iterations=2,
        )
        if result:
            print(f"   Eval ID: {result.id}")
            print(f"   Data: {result.eval_data}")
    except Exception as e:
        print(f"   Error: {e}")

    # List evals
    print("\n3. Listing eval runs...")
    try:
        evals = await client.list_eval_runs()
        for e in evals.data[:5]:
            print(f"   {e.id}: {e.eval_type} — {e.name}")
    except Exception as e:
        print(f"   Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
