"""Broadcast Mode

Same task is sent to every agent in the team. Moderator synthesizes the answer.
"""

from agno.agent import Agent
from agno.team.team import Team, TeamMode

from cookbook_config import model

proponent = Agent(
    name="Proponent",
    role="Argue FOR the proposition. Be concise: thesis, 2-3 points, conclusion.",
    model=model,
)

opponent = Agent(
    name="Opponent",
    role="Argue AGAINST the proposition. Be concise: thesis, 2-3 points, conclusion.",
    model=model,
)

team = Team(
    name="Structured Debate",
    mode=TeamMode.broadcast,
    model=model,
    members=[proponent, opponent],
    instructions=["Synthesize responses: highlight points for, against, areas of agreement, and the verdict"],
    show_members_responses=True,
    markdown=True,
)

if __name__ == "__main__":
    team.print_response("Remote work is better than in-office work for software teams.", stream=True)
