"""
Weave Integration
=================

Demonstrates logging Agno model calls with Weave.
"""

import weave
from agno.agent import Agent

from cookbook_config import model

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
weave.init("agno")


# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(model=model, markdown=True, debug_mode=True)


@weave.op()
def run(content: str):
    return agent.run(content)


# ---------------------------------------------------------------------------
# Run Example
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run("Share a 2 sentence horror story")
