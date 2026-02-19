"""Seltz Tools Example.

Run `pip install seltz agno openai python-dotenv` to install dependencies.
"""

from agno.agent import Agent
from agno.tools.seltz import SeltzTools
from dotenv import load_dotenv

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------


load_dotenv()

agent = Agent(
    model=model,
    tools=[SeltzTools(show_results=True)],
    markdown=True,
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent.print_response("Search for current AI safety reports", markdown=True)
