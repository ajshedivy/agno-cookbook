"""
Reasoning With Model
=============================

Use a separate reasoning model with configurable step limits.
"""

from agno.agent import Agent

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=model,
    # Use a separate model for the reasoning/thinking step
    reasoning_model=model,
    reasoning=True,
    reasoning_min_steps=2,
    reasoning_max_steps=5,
    markdown=True,
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(
        "A farmer has 17 sheep. All but 9 die. How many sheep are left?",
        stream=True,
        show_full_reasoning=True,
    )
