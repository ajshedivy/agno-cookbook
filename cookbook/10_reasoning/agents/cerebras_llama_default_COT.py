"""
Cerebras Default COT Fallback
=============================

Demonstrates default chain-of-thought behavior with a Cerebras model.
"""

from agno.agent import Agent

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
reasoning_agent = Agent(
    model=model,
    reasoning=True,
    debug_mode=True,
    markdown=True,
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    reasoning_agent.print_response(
        "Give me steps to write a python script for fibonacci series",
        stream=True,
        show_full_reasoning=True,
    )
