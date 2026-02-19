"""
Cache Team Response
=============================

Demonstrates two-layer caching for team leader and member responses.
"""

from agno.agent import Agent
from agno.team import Team

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Members
# ---------------------------------------------------------------------------
researcher = Agent(
    name="Researcher",
    role="Research and gather information",
    model=model,
)

writer = Agent(
    name="Writer",
    role="Write clear and engaging content",
    model=model,
)

# ---------------------------------------------------------------------------
# Create Team
# ---------------------------------------------------------------------------
content_team = Team(
    members=[researcher, writer],
    model=model,
    markdown=True,
    debug_mode=True,
)

# ---------------------------------------------------------------------------
# Run Team
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    content_team.print_response("Write a very very very explanation of caching in software")
