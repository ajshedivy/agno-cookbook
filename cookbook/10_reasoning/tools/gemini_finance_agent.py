"""
Gemini Finance Agent
====================

Demonstrates this reasoning cookbook example.
"""
# ! pip install -U agno

from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

from cookbook_config import model


# ---------------------------------------------------------------------------
# Create Example
# ---------------------------------------------------------------------------
def run_example() -> None:
    thinking_agent = Agent(
        model=model,
        tools=[
            ReasoningTools(add_instructions=True),
            YFinanceTools(),
        ],
        instructions="Use tables where possible",
        markdown=True,
        stream_events=True,
    )
    thinking_agent.print_response(
        "Write a report comparing NVDA to TSLA in detail",
        stream=True,
        show_reasoning=True,
    )


# ---------------------------------------------------------------------------
# Run Example
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()
