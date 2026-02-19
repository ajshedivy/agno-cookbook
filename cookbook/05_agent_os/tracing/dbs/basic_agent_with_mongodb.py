"""
Traces with AgentOS
Requirements:
    uv pip install agno opentelemetry-api opentelemetry-sdk openinference-instrumentation-agno
"""

from agno.agent import Agent
from agno.db.mongo import MongoDb
from agno.os import AgentOS
from agno.tools.hackernews import HackerNewsTools

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Example
# ---------------------------------------------------------------------------

# docker run -d -p 27017:27017 --name mongodb mongo:latest
db_url = "mongodb://localhost:27017"

db = MongoDb(db_url=db_url)

agent = Agent(
    name="HackerNews Agent",
    model=model,
    tools=[HackerNewsTools()],
    instructions="You are a hacker news agent. Answer questions concisely.",
    markdown=True,
    db=db,
)

# Setup our AgentOS app
agent_os = AgentOS(
    description="Example app for tracing HackerNews",
    agents=[agent],
    tracing=True,
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# Run Example
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="basic_agent_with_mongodb:app", reload=True)
