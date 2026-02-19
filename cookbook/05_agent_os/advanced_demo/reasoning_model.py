"""
Example showing a reasoning Agent in the AgentOS.

You can interact with the Agent as normally. It will reason before providing a final answer.
You will see its chain of thought live as it is generated.
"""

from agno.agent import Agent
from agno.os import AgentOS
from agno.run.agent import RunEvent  # noqa

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Example
# ---------------------------------------------------------------------------

# Create an agent with reasoning enabled
agent = Agent(
    reasoning_model=model,
    reasoning=True,
    instructions="Think step by step about the problem.",
)

# Setup our AgentOS app
agent_os = AgentOS(
    description="Reasoning model streaming",
    agents=[agent],
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# Run Example
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """Run your AgentOS.

    You can see the configuration and available apps at:
    http://localhost:7777/config

    """
    agent_os.serve(app="reasoning_model:app", reload=True)
