"""
Basic Coordination
=============================

Demonstrates a simple two-member team working together on one task.
"""

from agno.agent import Agent
from agno.team import Team

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Members
# ---------------------------------------------------------------------------
planner = Agent(
    name="Planner",
    role="You plan tasks and split work into clear, ordered steps.",
    model=model,
)

writer = Agent(
    name="Writer",
    role="You draft concise, readable summaries from the team discussion.",
    model=model,
)

# ---------------------------------------------------------------------------
# Create Team
# ---------------------------------------------------------------------------
team = Team(
    model=model,
    name="Planning Team",
    members=[planner, writer],
    instructions=[
        "Coordinate with the two members to answer the user question.",
        "First plan the response, then generate a clear final summary.",
    ],
    markdown=True,
    show_members_responses=True,
)


# ---------------------------------------------------------------------------
# Run Team
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    team.print_response(
        "Create a three-step outline for launching a small coding side project.",
        stream=True,
    )
