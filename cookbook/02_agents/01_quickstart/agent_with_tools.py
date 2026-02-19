"""
Agent With Tools
=============================

Agent With Tools Quickstart.
"""

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(
    name="Tool-Enabled Agent",
    model=model,
    tools=[DuckDuckGoTools()],
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response("Find one recent AI safety headline and summarize it.", stream=True)
