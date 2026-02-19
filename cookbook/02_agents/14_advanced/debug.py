"""
Debug
=============================

Debug.
"""

from agno.agent import Agent

from cookbook_config import model

# You can set the debug mode on the agent for all runs to have more verbose output
# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=model,
    debug_mode=True,
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(input="Tell me a joke.")

    # You can also set the debug mode on a single run
    agent = Agent(
        model=model,
    )
    agent.print_response(input="Tell me a joke.", debug_mode=True)
