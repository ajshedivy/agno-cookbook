"""
Run workflows via AgentOSClient — streaming and non-streaming.

Prerequisites:
1. Start an AgentOS server with workflows configured
2. Run this script: python run_workflows.py
"""

import asyncio

from agno.client import AgentOSClient


async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.aget_config()
    if not config.workflows:
        print("No workflows available")
        return

    workflow_id = config.workflows[0].id
    print(f"Using workflow: {workflow_id}")

    # Non-streaming run
    print("\n--- Non-Streaming ---")
    try:
        result = await client.run_workflow(
            workflow_id=workflow_id,
            message="What are the benefits of Python for data science?",
        )
        print(f"Run ID: {result.run_id}")
        print(f"Content: {result.content}")
    except Exception as e:
        print(f"Error: {e}")

    # Streaming run
    print("\n--- Streaming ---")
    try:
        async for event in client.run_workflow_stream(
            workflow_id=workflow_id,
            message="Explain machine learning in simple terms.",
        ):
            if event.event == "RunContent" and hasattr(event, "content"):
                print(event.content, end="", flush=True)
            elif event.event == "WorkflowAgentCompleted" and hasattr(event, "content") and event.content:
                print(event.content, end="", flush=True)
        print()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
