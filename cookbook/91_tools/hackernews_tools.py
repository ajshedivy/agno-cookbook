"""
Hackernews Tools
=============================

Demonstrates hackernews tools.
"""

from agno.agent import Agent
from agno.tools.hackernews import HackerNewsTools

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------


agent = Agent(
    model=model,
    tools=[HackerNewsTools()],
    markdown=True,
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response("Write a report on trending startups and products.", stream=True)
