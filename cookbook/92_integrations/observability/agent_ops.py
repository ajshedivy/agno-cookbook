"""
AgentOps Integration
====================

Demonstrates logging Agno model calls with AgentOps.
"""

import agentops
from agno.agent import Agent

from cookbook_config import model

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
# Initialize AgentOps
agentops.init()


# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(model=model)


# ---------------------------------------------------------------------------
# Run Example
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    response = agent.run("Share a 2 sentence horror story")
    print(response.content)
