"""
Nested Teams
=============================

Demonstrates using teams as members in a higher-level coordinating team.
"""

from agno.agent import Agent
from agno.team import Team

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Members
# ---------------------------------------------------------------------------
research_agent = Agent(
    name="Research Agent",
    model=model,
    role="Gather references and source material",
)

analysis_agent = Agent(
    name="Analysis Agent",
    model=model,
    role="Extract key findings and implications",
)

writing_agent = Agent(
    name="Writing Agent",
    model=model,
    role="Draft polished narrative output",
)

editing_agent = Agent(
    name="Editing Agent",
    model=model,
    role="Improve clarity and structure",
)

research_team = Team(
    name="Research Team",
    members=[research_agent, analysis_agent],
    model=model,
    instructions=[
        "Collect relevant information and summarize evidence.",
        "Highlight key takeaways and uncertainties.",
    ],
)

writing_team = Team(
    name="Writing Team",
    members=[writing_agent, editing_agent],
    model=model,
    instructions=[
        "Draft and refine final output from provided research.",
        "Keep language concise and decision-oriented.",
    ],
)

# ---------------------------------------------------------------------------
# Create Team
# ---------------------------------------------------------------------------
parent_team = Team(
    name="Program Team",
    members=[research_team, writing_team],
    model=model,
    instructions=[
        "Coordinate nested teams to deliver a single coherent response.",
        "Ask Research Team for evidence first, then Writing Team for synthesis.",
    ],
    markdown=True,
    show_members_responses=True,
)

# ---------------------------------------------------------------------------
# Run Team
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parent_team.print_response(
        "Prepare a one-page brief on adopting AI coding assistants in a startup engineering team.",
        stream=True,
    )
