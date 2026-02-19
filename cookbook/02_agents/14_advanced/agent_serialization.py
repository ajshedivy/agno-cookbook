"""
Agent Serialization
=============================

Agent Serialization.
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb

from cookbook_config import model

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="tmp/agents.db")

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(
    id="serialization-demo-agent",
    name="Serialization Demo Agent",
    model=model,
    db=agent_db,
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    config = agent.to_dict()
    recreated = Agent.from_dict(config)

    version = agent.save()
    loaded = Agent.load(id=agent.id, db=agent_db, version=version)

    recreated.print_response("Say hello from a recreated agent.", stream=True)
    loaded.print_response("Say hello from a loaded agent.", stream=True)
