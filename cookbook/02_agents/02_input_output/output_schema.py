"""
Output Schema
=============================

This example shows how to use the output_model parameter to specify the model that will be used to generate the final response.
"""

from agno.agent import Agent
from agno.tools.websearch import WebSearchTools

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=model,
    output_model=model,
    tools=[WebSearchTools()],
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response("Latest news from France?", stream=True)
