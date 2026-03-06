#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["agno[os]"]
# ///
"""
Run and manage agent evaluations on an AgentOS instance.

Examples:
    # List all evaluation runs
    uv run run_evals.py

    # Run an accuracy eval
    uv run run_evals.py --agent-id my-agent --accuracy --input "What is 2+2?" --expected "4"

    # Run a performance eval
    uv run run_evals.py --agent-id my-agent --performance --input "Hello" --iterations 3

    # Get details for a specific eval
    uv run run_evals.py --eval-id abc-123

    # Filter evals by agent
    uv run run_evals.py --agent-id my-agent

    # Use a different server
    uv run run_evals.py --base-url http://my-server:8000
"""

import argparse
import asyncio
import sys

from agno.client import AgentOSClient
from agno.db.schemas.evals import EvalType


async def list_evals(client: AgentOSClient, agent_id: str | None) -> None:
    evals = await client.list_eval_runs()
    items = evals.data or []
    if agent_id:
        items = [e for e in items if getattr(e, "agent_id", None) == agent_id]

    if not items:
        print("No evaluations found")
        return

    print(f"Found {len(items)} evaluation(s):\n")
    for e in items:
        print(f"  [{e.id}]")
        print(f"    type: {e.eval_type} | agent: {e.agent_id}")
        if e.name:
            print(f"    name: {e.name}")
        print()


async def run_accuracy_eval(
    client: AgentOSClient,
    agent_id: str,
    input_text: str,
    expected: str,
) -> None:
    result = await client.run_eval(
        agent_id=agent_id,
        eval_type=EvalType.ACCURACY,
        input_text=input_text,
        expected_output=expected,
    )
    if result:
        print(f"Eval ID: {result.id}")
        print(f"Type: {result.eval_type}")
        print(f"Data: {result.eval_data}")
    else:
        print("Evaluation returned no result")


async def run_performance_eval(
    client: AgentOSClient,
    agent_id: str,
    input_text: str,
    iterations: int,
) -> None:
    result = await client.run_eval(
        agent_id=agent_id,
        eval_type=EvalType.PERFORMANCE,
        input_text=input_text,
        num_iterations=iterations,
    )
    if result:
        print(f"Eval ID: {result.id}")
        print(f"Type: {result.eval_type}")
        print(f"Performance Data: {result.eval_data}")
    else:
        print("Evaluation returned no result")


async def get_eval_detail(client: AgentOSClient, eval_id: str) -> None:
    eval_run = await client.get_eval_run(eval_id)
    print(f"Eval: {eval_run.id}")
    print(f"  type: {eval_run.eval_type}")
    print(f"  agent: {eval_run.agent_id}")
    print(f"  model: {getattr(eval_run, 'model_id', 'N/A')}")
    print(f"  name: {eval_run.name}")
    print(f"  data: {eval_run.eval_data}")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run evals via AgentOS API")
    parser.add_argument("--base-url", default="http://localhost:7777", help="AgentOS server URL (default: http://localhost:7777)")
    parser.add_argument("--agent-id", help="Agent ID to evaluate or filter by")
    parser.add_argument("--eval-id", help="Get details for a specific evaluation")
    parser.add_argument("--accuracy", action="store_true", help="Run an accuracy evaluation")
    parser.add_argument("--performance", action="store_true", help="Run a performance evaluation")
    parser.add_argument("--input", dest="input_text", help="Input text for evaluation")
    parser.add_argument("--expected", help="Expected output (for --accuracy)")
    parser.add_argument("--iterations", type=int, default=3, help="Number of iterations (for --performance, default: 3)")
    args = parser.parse_args()

    client = AgentOSClient(base_url=args.base_url)

    if args.eval_id:
        await get_eval_detail(client, args.eval_id)
    elif args.accuracy:
        if not args.agent_id or not args.input_text or not args.expected:
            print("--accuracy requires --agent-id, --input, and --expected", file=sys.stderr)
            sys.exit(1)
        await run_accuracy_eval(client, args.agent_id, args.input_text, args.expected)
    elif args.performance:
        if not args.agent_id or not args.input_text:
            print("--performance requires --agent-id and --input", file=sys.stderr)
            sys.exit(1)
        await run_performance_eval(client, args.agent_id, args.input_text, args.iterations)
    else:
        await list_evals(client, args.agent_id)


if __name__ == "__main__":
    asyncio.run(main())
