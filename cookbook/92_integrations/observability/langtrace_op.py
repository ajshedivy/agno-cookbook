"""
Langtrace Integration
=====================

Demonstrates instrumenting an Agno agent with Langtrace.
"""

# Must precede other imports
from agno.agent import Agent
from agno.tools.yfinance import YFinanceTools
from langtrace_python_sdk import langtrace  # type: ignore

from cookbook_config import model

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
langtrace.init()


# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(
    name="Stock Price Agent",
    model=model,
    tools=[YFinanceTools()],
    instructions="You are a stock price agent. Answer questions in the style of a stock analyst.",
    debug_mode=True,
)


# ---------------------------------------------------------------------------
# Run Example
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response("What is the current price of Tesla?")
