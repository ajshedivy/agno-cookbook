# /// script
# requires-python = ">=3.11"
# dependencies = ["agno[openai]"]
# ///
"""
Reasoning Demo
===============
Self-contained demo of chain-of-thought reasoning with ReasoningTools.

Usage:
    export OPENAI_API_KEY=sk-...
    uv run reasoning_demo.py
    uv run reasoning_demo.py --model "anthropic:claude-sonnet-4-5"
    uv run reasoning_demo.py --problem "How many r's in strawberry?"
"""

import argparse

from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools

# ---------------------------------------------------------------------------
# Problems to solve
# ---------------------------------------------------------------------------
DEMO_PROBLEMS = [
    "How many r's are in the word 'strawberry'?",
    "A farmer has 17 sheep. All but 9 die. How many are left?",
    "If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?",
]


def main():
    parser = argparse.ArgumentParser(description="Reasoning demo")
    parser.add_argument(
        "--model",
        default="openai:gpt-4o",
        help="Model string, e.g. 'openai:gpt-4o' or 'anthropic:claude-sonnet-4-5'",
    )
    parser.add_argument(
        "--problem",
        default=None,
        help="Custom problem to solve (overrides built-in demos)",
    )
    args = parser.parse_args()

    # Agent WITH reasoning
    reasoning_agent = Agent(
        name="Reasoning Agent",
        model=args.model,
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            "Think through problems step by step.",
            "Show your reasoning clearly before giving the final answer.",
        ],
        markdown=True,
    )

    # Agent WITHOUT reasoning (for comparison)
    basic_agent = Agent(
        name="Basic Agent",
        model=args.model,
        markdown=True,
    )

    problems = [args.problem] if args.problem else DEMO_PROBLEMS

    for i, problem in enumerate(problems, 1):
        print(f"{'='*60}")
        print(f"Problem {i}: {problem}")
        print(f"{'='*60}")

        print("\n--- Without Reasoning ---\n")
        basic_agent.print_response(problem, stream=True)

        print("\n\n--- With ReasoningTools ---\n")
        reasoning_agent.print_response(problem, stream=True)

        print("\n")


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
