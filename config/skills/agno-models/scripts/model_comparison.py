# /// script
# requires-python = ">=3.11"
# dependencies = ["agno[openai]"]
# ///
"""
Model Comparison Demo
======================
Self-contained demo comparing multiple model providers on the same prompts.
Install additional provider extras to compare more models.

Usage:
    export OPENAI_API_KEY=sk-...
    uv run model_comparison.py

    # Compare specific models
    uv run model_comparison.py --models "openai:gpt-4o" "openai:gpt-4o-mini"

    # With Anthropic
    pip install "agno[anthropic]"
    export ANTHROPIC_API_KEY=sk-ant-...
    uv run model_comparison.py --models "openai:gpt-4o" "anthropic:claude-sonnet-4-5"
"""

import argparse
import time

from agno.agent import Agent

# ---------------------------------------------------------------------------
# Test prompts
# ---------------------------------------------------------------------------
TEST_PROMPTS = [
    {
        "name": "Factual",
        "prompt": "What is the capital of Australia? Reply in one sentence.",
    },
    {
        "name": "Reasoning",
        "prompt": "A bat and a ball cost $1.10. The bat costs $1.00 more than the ball. How much does the ball cost? Show your reasoning.",
    },
    {
        "name": "Creative",
        "prompt": "Write a haiku about debugging code.",
    },
]


def run_comparison(models: list[str], prompts: list[dict]):
    """Run each prompt through each model and display results."""
    for test in prompts:
        print(f"\n{'='*60}")
        print(f"Test: {test['name']}")
        print(f"Prompt: {test['prompt']}")
        print(f"{'='*60}")

        for model_id in models:
            print(f"\n--- {model_id} ---\n")

            try:
                agent = Agent(model=model_id, markdown=True)
                start = time.time()
                response = agent.run(test["prompt"])
                elapsed = time.time() - start

                print(f"{response.content}")
                print(f"\n  [Time: {elapsed:.2f}s]")

                if response.metrics:
                    tokens = getattr(response.metrics, "total_tokens", None)
                    if tokens:
                        print(f"  [Tokens: {tokens}]")

            except ImportError as e:
                print(f"  [SKIPPED] Missing provider: {e}")
            except Exception as e:
                print(f"  [ERROR] {e}")


def main():
    parser = argparse.ArgumentParser(description="Model comparison demo")
    parser.add_argument(
        "--models",
        nargs="+",
        default=["openai:gpt-4o", "openai:gpt-4o-mini"],
        help="Model strings to compare (space-separated)",
    )
    args = parser.parse_args()

    print("Model Comparison")
    print(f"Models: {', '.join(args.models)}")

    run_comparison(args.models, TEST_PROMPTS)

    print(f"\n{'='*60}")
    print("Comparison complete.")


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
