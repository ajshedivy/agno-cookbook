"""
Async Tools
===========

Demonstrates async team execution with mixed research and scraping tools.
"""

import asyncio
from uuid import uuid4

from agno.agent import Agent
from agno.team import Team
from agno.tools.agentql import AgentQLTools
from agno.tools.websearch import WebSearchTools
from agno.tools.wikipedia import WikipediaTools

from cookbook_config import model

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
custom_query = """
{
    title
    text_content[]
}
"""

# ---------------------------------------------------------------------------
# Create Members
# ---------------------------------------------------------------------------
wikipedia_agent = Agent(
    name="Wikipedia Agent",
    role="Search wikipedia for information",
    model=model,
    tools=[WikipediaTools()],
    instructions=[
        "Find information about the company in the wikipedia",
    ],
)

website_agent = Agent(
    name="Website Agent",
    role="Search the website for information",
    model=model,
    tools=[WebSearchTools()],
    instructions=[
        "Search the website for information",
    ],
)

# ---------------------------------------------------------------------------
# Create Team
# ---------------------------------------------------------------------------
user_id = str(uuid4())
team_id = str(uuid4())

company_info_team = Team(
    name="Company Info Team",
    id=team_id,
    model=model,
    tools=[AgentQLTools(agentql_query=custom_query)],
    members=[wikipedia_agent, website_agent],
    markdown=True,
    instructions=[
        "You are a team that finds information about a company.",
        "First search the web and wikipedia for information about the company.",
        "If you can find the company's website URL, then scrape the homepage and the about page.",
    ],
    show_members_responses=True,
)

# ---------------------------------------------------------------------------
# Run Team
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(
        company_info_team.aprint_response(
            "Write me a full report on everything you can find about Agno, the company building AI agent infrastructure.",
            stream=True,
        )
    )
