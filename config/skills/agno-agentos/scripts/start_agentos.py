"""
Start AgentOS - Template Script
================================
Quick-start template for launching an AgentOS instance.

Usage:
    python start_agentos.py

Prerequisites:
    pip install "agno[os,anthropic]"
    export ANTHROPIC_API_KEY=sk-...
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.tools.calculator import CalculatorTools

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/agentos.db")

agent = Agent(
    name="Assistant",
    model=Claude(id="claude-sonnet-4-5"),
    db=db,
    tools=[CalculatorTools()],
    instructions=["You are a helpful assistant."],
    markdown=True,
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True,
)

# ---------------------------------------------------------------------------
# AgentOS
# ---------------------------------------------------------------------------
agent_os = AgentOS(
    id="quickstart",
    description="Quick-start AgentOS instance",
    agents=[agent],
)

app = agent_os.get_app()

# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent_os.serve(app="start_agentos:app", reload=True)
