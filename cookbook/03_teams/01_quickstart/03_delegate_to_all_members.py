"""
Delegate To All Members
=============================

Demonstrates collaborative team execution with delegate-to-all behavior.
"""

import asyncio
from textwrap import dedent

from agno.agent import Agent
from agno.team import Team, TeamMode
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Members
# ---------------------------------------------------------------------------
reddit_researcher = Agent(
    name="Reddit Researcher",
    role="Research a topic on Reddit",
    model=model,
    tools=[WebSearchTools()],
    add_name_to_context=True,
    instructions=dedent("""
    You are a Reddit researcher.
    You will be given a topic to research on Reddit.
    You will need to find the most relevant posts on Reddit.
    """),
)

hackernews_researcher = Agent(
    name="HackerNews Researcher",
    model=model,
    role="Research a topic on HackerNews.",
    tools=[HackerNewsTools()],
    add_name_to_context=True,
    instructions=dedent("""
    You are a HackerNews researcher.
    You will be given a topic to research on HackerNews.
    You will need to find the most relevant posts on HackerNews.
    """),
)

# ---------------------------------------------------------------------------
# Create Team
# ---------------------------------------------------------------------------
agent_team = Team(
    name="Discussion Team",
    model=model,
    members=[
        reddit_researcher,
        hackernews_researcher,
    ],
    instructions=[
        "You are a discussion master.",
        "You have to stop the discussion when you think the team has reached a consensus.",
    ],
    markdown=True,
    mode=TeamMode.broadcast,
    show_members_responses=True,
)


async def run_async_collaboration() -> None:
    await agent_team.aprint_response(
        input="Start the discussion on the topic: 'What is the best way to learn to code?'",
        stream=True,
    )


# ---------------------------------------------------------------------------
# Run Team
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- Sync ---
    agent_team.print_response(
        input="Start the discussion on the topic: 'What is the best way to learn to code?'",
        stream=True,
    )

    # --- Async ---
    asyncio.run(run_async_collaboration())
