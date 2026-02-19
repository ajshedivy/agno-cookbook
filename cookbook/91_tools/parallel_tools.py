"""
Parallel Tools
=============================

Demonstrates parallel tools.
"""

from agno.agent import Agent
from agno.tools.parallel import ParallelTools

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------


agent = Agent(
    model=model,
    tools=[ParallelTools()],
    instructions="No need to tell me its based on your research.",
    markdown=True,
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(
        "Tell me about Agno's AgentOS?",
        stream=True,
        stream_events=True,
    )
