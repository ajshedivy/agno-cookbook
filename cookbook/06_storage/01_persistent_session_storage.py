"""
Persistent Session Storage
==========================

Demonstrates using PostgresDb for persistent session storage with a team.
"""

from agno.agent.agent import Agent
from agno.db.postgres import PostgresDb
from agno.team.team import Team

from cookbook_config import model

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url=db_url, session_table="sessions")

# ---------------------------------------------------------------------------
# Create Team
# ---------------------------------------------------------------------------
agent = Agent(name="test_agent", model=model)
team = Team(
    members=[agent],
    db=db,
    session_id="team_session_storage",
    add_history_to_context=True,
)

# ---------------------------------------------------------------------------
# Run Team
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    team.print_response("Tell me a new interesting fact about space")
