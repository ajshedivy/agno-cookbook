"""
JSON Schema Output
==================

Demonstrates provider-native JSON schema output for team responses.
"""

from agno.agent import Agent
from agno.team import Team, TeamMode
from agno.tools.websearch import WebSearchTools
from agno.utils.pprint import pprint_run_response

from cookbook_config import model

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
stock_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "StockAnalysis",
        "schema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "Stock ticker symbol"},
                "company_name": {"type": "string", "description": "Company name"},
                "analysis": {"type": "string", "description": "Brief analysis"},
            },
            "required": ["symbol", "company_name", "analysis"],
            "additionalProperties": False,
        },
    },
}

# ---------------------------------------------------------------------------
# Create Members
# ---------------------------------------------------------------------------
stock_searcher = Agent(
    name="Stock Searcher",
    model=model,
    role="Searches for information on stocks and provides price analysis.",
    tools=[WebSearchTools()],
)

company_info_agent = Agent(
    name="Company Info Searcher",
    model=model,
    role="Searches for information about companies and recent news.",
    tools=[WebSearchTools()],
)

# ---------------------------------------------------------------------------
# Create Team
# ---------------------------------------------------------------------------
team = Team(
    name="Stock Research Team",
    model=model,
    mode=TeamMode.route,
    members=[stock_searcher, company_info_agent],
    output_schema=stock_schema,
    use_json_mode=True,
    markdown=True,
)

# ---------------------------------------------------------------------------
# Run Team
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    response = team.run("What is the current stock price of NVDA?")
    assert isinstance(response.content, dict)
    assert response.content_type == "dict"
    pprint_run_response(response)
