"""
Team Introduction
=============================

Demonstrates setting a reusable team introduction message for a session.
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.team import Team

from cookbook_config import model

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/teams.db", session_table="team_sessions")
INTRODUCTION = "Hello, I'm your personal assistant. I can help you only with questions related to mountain climbing."

# ---------------------------------------------------------------------------
# Create Members
# ---------------------------------------------------------------------------
agent = Agent(
    model=model,
)

# ---------------------------------------------------------------------------
# Create Team
# ---------------------------------------------------------------------------
team = Team(
    model=model,
    db=db,
    members=[agent],
    introduction=INTRODUCTION,
    session_id="introduction_session_mountain_climbing",
    add_history_to_context=True,
)

# ---------------------------------------------------------------------------
# Run Team
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    team.print_response("Easiest 14er in USA?")
    team.print_response("Is K2 harder to climb than Everest?")
