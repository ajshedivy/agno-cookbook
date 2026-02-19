"""
CodingTools: All 7 Tools Enabled
=================================
Enable all tools including the exploration tools (grep, find, ls)
by setting all=True or enabling them individually.
"""

from agno.agent import Agent
from agno.tools.coding import CodingTools

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Agent with all CodingTools
# ---------------------------------------------------------------------------
agent = Agent(
    model=model,
    tools=[CodingTools(base_dir=".", all=True)],
    instructions="You are a coding assistant. Use the coding tools to help the user.",
    markdown=True,
)

# ---------------------------------------------------------------------------
# Run Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(
        "Find all Python files in this directory, then grep for any import statements.",
        stream=True,
    )
