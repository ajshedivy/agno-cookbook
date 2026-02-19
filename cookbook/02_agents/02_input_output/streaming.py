"""
Streaming
=============================

Demonstrates streaming agent responses token by token.
"""

from agno.agent import Agent

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=model,
    markdown=True,
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Stream the response token by token
    agent.print_response(
        "Explain the difference between concurrency and parallelism.",
        stream=True,
    )
