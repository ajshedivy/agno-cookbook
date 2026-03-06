---
name: agno-agentos
description: |
  Deploy Agno agents as production APIs using AgentOS. Covers FastAPI
  integration, database configuration, knowledge registration, and
  serving. Trigger this skill when: importing agno.os, creating AgentOS
  instances, deploying agents to production, serving agents via API,
  or asking "how do I deploy an Agno agent?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["agentos", "deployment", "agno", "fastapi", "production"]
---

# Deploy with AgentOS

Use `agno.os.AgentOS` to serve agents, teams, and workflows as production APIs. Install with `pip install "agno[os]"`.

## Quick Start

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.os import AgentOS

agent = Agent(
    name="My Agent",
    model=Claude(id="claude-sonnet-4-5"),
    instructions="You are a helpful assistant.",
)

agent_os = AgentOS(agents=[agent])
agent_os.serve()
```

Run with: `python app.py` — serves at `http://localhost:7777`.

## Full Setup with Agents, Teams, and Workflows

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.db.sqlite import SqliteDb
from agno.os import AgentOS
from agno.team.team import Team
from agno.tools.calculator import CalculatorTools
from agno.tools.websearch import WebSearchTools
from agno.workflow.step import Step
from agno.workflow.workflow import Workflow

# Database
db = SqliteDb(db_file="tmp/app.db")

# Agents
assistant = Agent(
    name="Assistant",
    model=Claude(id="claude-sonnet-4-5"),
    db=db,
    tools=[CalculatorTools()],
    instructions=["You are a helpful assistant."],
    markdown=True,
    update_memory_on_run=True,
    add_history_to_context=True,
    num_history_runs=3,
)

researcher = Agent(
    name="Researcher",
    model=Claude(id="claude-sonnet-4-5"),
    db=db,
    tools=[WebSearchTools()],
    instructions=["You are a research assistant."],
    markdown=True,
)

# Team
research_team = Team(
    name="Research Team",
    model=Claude(id="claude-sonnet-4-5"),
    members=[assistant, researcher],
    instructions=["Coordinate research tasks."],
    db=db,
    markdown=True,
)

# Workflow
qa_workflow = Workflow(
    name="QA Workflow",
    description="Simple Q&A workflow",
    db=db,
    steps=[Step(name="Answer", agent=assistant)],
)

# AgentOS
agent_os = AgentOS(
    id="my-app",
    description="My production agent application",
    agents=[assistant, researcher],
    teams=[research_team],
    workflows=[qa_workflow],
)

app = agent_os.get_app()  # Returns FastAPI app

if __name__ == "__main__":
    agent_os.serve(app="app:app", reload=True)
```

## AgentOS Parameters

```python
AgentOS(
    id="app-id",                          # Unique application ID
    description="What this app does",     # Description
    agents=[agent1, agent2],              # Agents to serve
    teams=[team1],                        # Teams to serve
    workflows=[workflow1],                # Workflows to serve
    knowledge=[knowledge1],              # Knowledge bases (enables upload/search endpoints)
)
```

## Serving Options

```python
# Quick start (blocks, good for development)
agent_os.serve()

# With uvicorn options
agent_os.serve(app="module:app", reload=True)

# Get FastAPI app for custom hosting
app = agent_os.get_app()

# Then run with uvicorn directly:
# uvicorn module:app --reload --port 7777
# Or: fastapi dev module.py
```

## Database Configuration

**Development (SQLite):**
```python
from agno.db.sqlite import SqliteDb
db = SqliteDb(db_file="tmp/app.db")
```

**Production (PostgreSQL):**
```python
from agno.db.postgres import PostgresDb
db = PostgresDb(db_url="postgresql+psycopg://user:pass@host:5432/dbname")
```

## Knowledge Base Registration

Register knowledge bases to enable search and upload endpoints:

```python
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.vectordb.chroma import ChromaDb

knowledge = Knowledge(
    vector_db=ChromaDb(
        path="tmp/chromadb",
        collection="docs",
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
    contents_db=db,  # Required for upload/management endpoints
)

agent = Agent(
    name="Knowledge Agent",
    knowledge=knowledge,
    search_knowledge=True,
)

agent_os = AgentOS(
    agents=[agent],
    knowledge=[knowledge],  # Registers knowledge API endpoints
)
```

## Skills Integration

Load skills into agents served via AgentOS:

```python
from pathlib import Path
from agno.skills import LocalSkills, Skills

skills_dir = Path(__file__).parent / "skills"

agent = Agent(
    name="Skills Agent",
    model=Claude(id="claude-sonnet-4-5"),
    skills=Skills(loaders=[LocalSkills(str(skills_dir))]),
)

agent_os = AgentOS(agents=[agent])
```

## API Endpoints

After starting AgentOS, explore endpoints at:
- `http://localhost:7777/docs` — Swagger UI
- `http://localhost:7777/config` — Configuration and available agents/teams/workflows

## Anti-Patterns

- **Don't skip `db=`** on agents — without storage, sessions don't persist between API calls
- **Don't forget `contents_db=` on Knowledge** — required for content upload endpoints
- **Don't use SQLite in production** — use PostgreSQL for multi-server deployments
- **Don't forget to install extras**: `pip install "agno[os]"` for AgentOS features
- **Don't hardcode secrets** — use environment variables for API keys and database URLs

## Further Reading

For advanced AgentOS configuration and deployment patterns, read `references/api-patterns.md`.
