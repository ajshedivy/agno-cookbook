"""Run `uv pip install openai ddgs yfinance` to install dependencies."""

from agno.agent import Agent
from agno.tools.websearch import WebSearchTools
from agno.tools.yfinance import YFinanceTools

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------


agent = Agent(
    model=model,
    tools=[WebSearchTools(), YFinanceTools()],
    instructions=["Use tables to display data"],
    markdown=True,
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(
        "Write a thorough report on NVDA, get all financial information and latest news",
        stream=True,
    )
