"""
Instructions
=============================

Instructions.
"""

from agno.agent import Agent

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=model,
    add_datetime_to_context=True,
    timezone_identifier="Etc/UTC",
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response("What is the current date and time? What is the current time in NYC?")
