# /// script
# requires-python = ">=3.11"
# dependencies = ["agno[os,anthropic]"]
# ///
"""
Start AgentOS - Template Script
================================
Quick-start template for launching an AgentOS instance.

Usage:
    export ANTHROPIC_API_KEY=sk-...
    uv run start_agentos.py
    uv run start_agentos.py --port 8000
"""

import argparse

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
    parser = argparse.ArgumentParser(description="Start an AgentOS server")
    parser.add_argument("--port", type=int, default=7777, help="Port to serve on (default: 7777)")
    args = parser.parse_args()

    agent_os.serve(app="start_agentos:app", reload=True, port=args.port)
