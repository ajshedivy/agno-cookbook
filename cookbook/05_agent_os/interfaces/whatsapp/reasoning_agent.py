"""
Reasoning Agent
===============

Demonstrates reasoning agent.
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.os.app import AgentOS
from agno.os.interfaces.whatsapp import Whatsapp
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Example
# ---------------------------------------------------------------------------

agent_db = SqliteDb(db_file="tmp/persistent_memory.db")

reasoning_finance_agent = Agent(
    name="Reasoning Finance Agent",
    model=model,
    db=agent_db,
    tools=[
        ReasoningTools(add_instructions=True),
        YFinanceTools(),
    ],
    instructions="Use tables to display data. When you use thinking tools, keep the thinking brief.",
    add_datetime_to_context=True,
    markdown=True,
)


# Setup our AgentOS app
agent_os = AgentOS(
    agents=[reasoning_finance_agent],
    interfaces=[Whatsapp(agent=reasoning_finance_agent)],
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
    agent_os.serve(app="reasoning_agent:app", reload=True)
