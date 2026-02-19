"""
Claude Reasoning Tools
======================

Demonstrates this reasoning cookbook example.
"""

from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools
from agno.tools.websearch import WebSearchTools

from cookbook_config import model


# ---------------------------------------------------------------------------
# Create Example
# ---------------------------------------------------------------------------
def run_example() -> None:
    reasoning_agent = Agent(
        model=model,
        tools=[
            ReasoningTools(add_instructions=True),
            WebSearchTools(enable_news=False),
        ],
        instructions="Use tables to display data.",
        markdown=True,
    )

    # Semiconductor market analysis example
    reasoning_agent.print_response(
        """\
        Analyze the semiconductor market performance focusing on:
        - NVIDIA (NVDA)
        - AMD (AMD)
        - Intel (INTC)
        - Taiwan Semiconductor (TSM)
        Compare their market positions, growth metrics, and future outlook.""",
        stream=True,
        show_full_reasoning=True,
    )


# ---------------------------------------------------------------------------
# Run Example
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()
