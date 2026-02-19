"""
Output Model
============

Demonstrates setting a dedicated model for final team response generation.
"""

from agno.agent import Agent
from agno.team import Team
from agno.tools.websearch import WebSearchTools

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Members
# ---------------------------------------------------------------------------
itinerary_planner = Agent(
    name="Itinerary Planner",
    model=model,
    description="You help people plan amazing vacations. Use the tools at your disposal to find latest information about the destination.",
    tools=[WebSearchTools()],
)

# ---------------------------------------------------------------------------
# Create Team
# ---------------------------------------------------------------------------
travel_expert = Team(
    model=model,
    members=[itinerary_planner],
    output_model=model,
)

# ---------------------------------------------------------------------------
# Run Team
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    travel_expert.print_response("Plan a summer vacation in Paris", stream=True)
