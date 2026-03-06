#!/usr/bin/env python3
"""
Discover and run workflows on an AgentOS instance.

Examples:
    # List all available workflows
    python run_workflows.py

    # Run a specific workflow
    python run_workflows.py --workflow-id qa-workflow --message "Explain machine learning"

    # Stream a workflow response
    python run_workflows.py --message "Analyze AI trends" --stream

    # Run against a remote server
    python run_workflows.py --base-url http://my-server:8000 --message "Process this"
"""

import argparse
import asyncio
import sys

from agno.client import AgentOSClient


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
    parser.add_argument("--workflow-id", help="Workflow ID to run (default: first available)")
    parser.add_argument("--message", "-m", help="Message to send to the workflow")
    parser.add_argument("--stream", "-s", action="store_true", help="Stream the response")
    args = parser.parse_args()

    client = AgentOSClient(base_url=args.base_url)

    if args.message:
        await run_workflow(client, args.workflow_id, args.message, args.stream)
    else:
        await list_workflows(client)


if __name__ == "__main__":
    asyncio.run(main())
