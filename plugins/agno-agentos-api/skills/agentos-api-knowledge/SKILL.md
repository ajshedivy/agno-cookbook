---
name: agentos-api-knowledge
description: |
  Interact with AgentOS Knowledge API endpoints using the AgentOSClient SDK.
  Use this skill to write ad-hoc Python scripts, tests, and automation
  for uploading content, searching the knowledge base, listing and
  deleting content, checking content status, and getting config. Trigger
  when: importing AgentOSClient to work with knowledge, writing scripts
  to upload documents, creating knowledge tests, or asking things like
  "upload this md file to my knowledge base" or "search my docs for X."
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["agentos", "knowledge", "api", "client", "agno"]
---

# AgentOS Knowledge API

Use `agno.client.AgentOSClient` to upload, search, list, and manage knowledge base content on a remote AgentOS instance. Only requires `uv` — all dependencies are declared inline via PEP 723.

## Prerequisites

Start an AgentOS server with knowledge configured:

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.db.sqlite import SqliteDb
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.vectordb.chroma import ChromaDb
from agno.os import AgentOS

db = SqliteDb(db_file="tmp/app.db")

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
    model=Claude(id="claude-sonnet-4-5"),
    knowledge=knowledge,
    search_knowledge=True,
    db=db,
)

agent_os = AgentOS(agents=[agent], knowledge=[knowledge])
agent_os.serve()
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/knowledge/config` | Get knowledge config |
| GET | `/knowledge/content` | List all content (paginated) |
| GET | `/knowledge/content/{content_id}` | Get content by ID |
| GET | `/knowledge/content/{content_id}/status` | Get content status |
| POST | `/knowledge/search` | Search knowledge base |
| POST | `/knowledge/content` | Upload content |
| PATCH | `/knowledge/content/{content_id}` | Update content metadata |
| DELETE | `/knowledge/content` | Delete all content |
| DELETE | `/knowledge/content/{content_id}` | Delete content by ID |

## Get Knowledge Config

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    config = await client.get_knowledge_config()
    print(f"Readers: {config.readers if hasattr(config, 'readers') else 'N/A'}")
    print(f"Chunkers: {config.chunkers if hasattr(config, 'chunkers') else 'N/A'}")

asyncio.run(main())
```

## Upload Text Content

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    result = await client.upload_knowledge_content(
        text_content="Agno is a framework for building AI agents and teams.",
        name="Agno Overview",
        description="Overview of the Agno framework",
    )

    print(f"Content ID: {result.id}")
    print(f"Status: {result.status}")
```

## Check Content Processing Status

Content is processed asynchronously. Check status after uploading:

```python
status = await client.get_content_status(content_id)
print(f"Status: {status.status}")
print(f"Message: {status.status_message}")
```

## List Content

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    content = await client.list_knowledge_content()
    print(f"Found {len(content.data)} content items")

    for item in content.data:
        print(f"  {item.id}: {item.name} ({item.status})")
```

Supports pagination via `limit` and `page` parameters, and sorting via `sort_by` and `sort_order`.

## Search Knowledge Base

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    results = await client.search_knowledge(
        query="What is Agno?",
        limit=5,
    )

    print(f"Found {len(results.data)} results")
    for result in results.data:
        preview = str(result.content)[:100] if hasattr(result, "content") else "N/A"
        score = result.score if hasattr(result, "score") else "N/A"
        print(f"  Score: {score} — {preview}...")
```

## Update Content Metadata

```python
updated = await client.update_content(
    content_id="content-id-here",
    name="Updated Name",
    description="Updated description",
)
```

## Delete Content

```python
# Delete specific content
await client.delete_content("content-id-here")

# Delete all content
await client.delete_all_content()
```

## Full Upload and Search Workflow

```python
import asyncio
from agno.client import AgentOSClient

async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    # Upload
    result = await client.upload_knowledge_content(
        text_content="""
        # Agno Framework Guide
        Agno is a powerful framework for building AI agents.
        Key features: agent creation, team coordination, workflows.
        """,
        name="Agno Guide",
        description="A guide to the Agno framework",
    )
    print(f"Uploaded: {result.id}")

    # Check status
    status = await client.get_content_status(result.id)
    print(f"Status: {status.status}")

    # Search
    results = await client.search_knowledge(query="What is Agno?", limit=5)
    for r in results.data:
        print(f"  {str(r.content)[:100]}...")

    # List
    content = await client.list_knowledge_content()
    print(f"Total items: {len(content.data)}")

asyncio.run(main())
```

## Anti-Patterns

- **Don't forget `contents_db=` on Knowledge** — required for upload/management endpoints
- **Don't forget `knowledge=[...]` on AgentOS** — registers knowledge API endpoints
- **Don't assume instant processing** — content is processed asynchronously; check status
- **Don't skip error handling** — knowledge endpoints may not be configured on all instances

## Further Reading

For advanced knowledge API patterns, read `references/api-patterns.md`.
