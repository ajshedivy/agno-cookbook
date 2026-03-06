# /// script
# requires-python = ">=3.11"
# dependencies = ["agno[openai]"]
# ///
"""
Guardrails Demo
================
Self-contained demo of input and output guardrails — validate messages
before and after agent processing.

Usage:
    export OPENAI_API_KEY=sk-...
    uv run guardrails_demo.py
    uv run guardrails_demo.py --model "anthropic:claude-sonnet-4-5"
"""

import argparse
import re

from agno.agent import Agent
from agno.exceptions import InputCheckError, OutputCheckError
from agno.guardrails.base import BaseGuardrail, BaseOutputGuardrail
from agno.run.agent import RunInput, RunOutput


# ---------------------------------------------------------------------------
# Custom guardrails
# ---------------------------------------------------------------------------
class LengthGuardrail(BaseGuardrail):
    """Block messages that are too short or too long."""

    min_length: int = 3
    max_length: int = 5000

    def check(self, run_input: RunInput):
        content = run_input.input_content_string()
        if len(content) < self.min_length:
            raise InputCheckError(
                f"Message too short (min {self.min_length} characters)"
            )
        if len(content) > self.max_length:
            raise InputCheckError(
                f"Message too long (max {self.max_length} characters)"
            )

    async def async_check(self, run_input: RunInput):
        self.check(run_input)


class SpamGuardrail(BaseGuardrail):
    """Block messages with excessive punctuation (likely spam)."""

    max_exclamations: int = 5

    def check(self, run_input: RunInput):
        content = run_input.input_content_string()
        if content.count("!") > self.max_exclamations:
            raise InputCheckError("Message appears to be spam")

    async def async_check(self, run_input: RunInput):
        self.check(run_input)


class NoEmailOutputGuardrail(BaseOutputGuardrail):
    """Prevent the agent from outputting email addresses."""

    def check(self, run_output: RunOutput):
        content = str(run_output.output_content_string())
        if re.search(r"\b[\w.-]+@[\w.-]+\.\w+\b", content):
            raise OutputCheckError("Output contains an email address")

    async def async_check(self, run_output: RunOutput):
        self.check(run_output)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Guardrails demo")
    parser.add_argument(
        "--model",
        default="openai:gpt-4o",
        help="Model string, e.g. 'openai:gpt-4o' or 'anthropic:claude-sonnet-4-5'",
    )
    args = parser.parse_args()

    agent = Agent(
        name="Guarded Agent",
        model=args.model,
        pre_hooks=[
            LengthGuardrail(),
            SpamGuardrail(),
        ],
        post_hooks=[
            NoEmailOutputGuardrail(),
        ],
        instructions=["You are a helpful assistant."],
        markdown=True,
    )

    # --- Test 1: Normal message (should pass) ---
    print("=== Test 1: Normal message ===\n")
    try:
        agent.print_response("What is the capital of France?", stream=True)
        print("\n[PASSED] Message accepted")
    except (InputCheckError, OutputCheckError) as e:
        print(f"\n[BLOCKED] {e}")

    # --- Test 2: Too short (should be blocked) ---
    print("\n\n=== Test 2: Too short ===\n")
    try:
        agent.print_response("Hi", stream=True)
        print("\n[PASSED] Message accepted")
    except InputCheckError as e:
        print(f"[BLOCKED] {e}")

    # --- Test 3: Spam (should be blocked) ---
    print("\n\n=== Test 3: Spam detection ===\n")
    try:
        agent.print_response("BUY NOW!!! BEST DEAL EVER!!!! CLICK HERE!!!", stream=True)
        print("\n[PASSED] Message accepted")
    except InputCheckError as e:
        print(f"[BLOCKED] {e}")

    # --- Test 4: Request that might trigger output guardrail ---
    print("\n\n=== Test 4: Output guardrail ===\n")
    try:
        agent.print_response(
            "Generate a fake contact card with a name and email.",
            stream=True,
        )
        print("\n[PASSED] Output accepted")
    except OutputCheckError as e:
        print(f"\n[BLOCKED] {e}")


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
