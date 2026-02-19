"""
Team With Agentic Memory
========================

Demonstrates team-level agentic memory creation and updates during runs.
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.team import Team

from cookbook_config import model

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url=db_url)
john_doe_id = "john_doe@example.com"

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
    members=[agent],
    db=db,
    enable_agentic_memory=True,
)

# ---------------------------------------------------------------------------
# Run Team
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    team.print_response(
        "My name is John Doe and I like to hike in the mountains on weekends.",
        stream=True,
        user_id=john_doe_id,
    )

    team.print_response("What are my hobbies?", stream=True, user_id=john_doe_id)
