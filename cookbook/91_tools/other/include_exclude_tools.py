"""
Include Exclude Tools
=============================

Demonstrates include exclude tools.
"""

import asyncio

from agno.agent import Agent
from agno.tools.calculator import CalculatorTools
from agno.tools.websearch import WebSearchTools

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------


agent = Agent(
    model=model,
    tools=[
        CalculatorTools(
            exclude_tools=["exponentiate", "factorial", "is_prime", "square_root"],
        ),
        WebSearchTools(include_tools=["web_search"]),
    ],
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(
        agent.aprint_response(
            "Search the web for a difficult sum that can be done with normal arithmetic and solve it.",
            markdown=True,
        )
    )
