"""
Basic Agent
=============================

Basic Agent Quickstart.
"""

from agno.agent import Agent

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(
    name="Quickstart Agent",
    model=model,
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response("Say hello and introduce yourself in one sentence.", stream=True)
