---
name: agentos-api-knowledge
description: |
  Interact with AgentOS Knowledge API endpoints. For standard operations
  (listing content, uploading files, searching, deleting), use the provided
  CLI script first. Only write custom Python when the script cannot handle
  the use case (e.g., pagination, updating metadata, bulk workflows,
  get config). Trigger when: uploading documents, searching the knowledge
  base, listing content, or asking things like "upload this md file to my
  knowledge base" or "search my docs for X."
license: Apache-2.0
metadata:
  version: "1.1.0"
  author: agno-team
  tags: ["agentos", "knowledge", "api", "client", "agno"]
---

# AgentOS Knowledge API

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

## Default: Use the CLI Script

**Always try the provided script first.** It covers listing content, uploading
files, uploading raw text, searching the knowledge base, checking processing
status, and deleting content — all from the command line with no custom code
needed.

The script is at: `scripts/manage_knowledge.py`

### List all content

```bash
uv run scripts/manage_knowledge.py --base-url http://localhost:7777
```

### Search the knowledge base

```bash
uv run scripts/manage_knowledge.py --base-url http://localhost:7777 \
  --search "What is Agno?" --limit 5
```

### Upload a text file

```bash
uv run scripts/manage_knowledge.py --base-url http://localhost:7777 \
  --upload README.md
```

### Upload raw text

```bash
uv run scripts/manage_knowledge.py --base-url http://localhost:7777 \
  --upload-text "Agno is an AI agent framework" --name "Agno Intro"
```

### Check processing status

```bash
uv run scripts/manage_knowledge.py --base-url http://localhost:7777 \
  --status content-id-123
```

### Delete specific content

```bash
uv run scripts/manage_knowledge.py --base-url http://localhost:7777 \
  --delete content-id-123
```

### Full CLI reference

```
uv run scripts/manage_knowledge.py --help
```

## When to Write Custom Python

Only write ad-hoc Python when the CLI script cannot handle your use case:

- **Get knowledge config** (readers, chunkers, embedder info)
- **Pagination and sorting** when listing content
- **Update content metadata** (name, description)
- **Delete all content** at once
- **Chaining multiple operations** in a single script (e.g., upload then search)
- **Custom error handling** or retry logic
- **Integration tests** that assert on response content

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

## Custom Python Examples

### Get Knowledge Config

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

### List Content with Pagination

```python
async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    content = await client.list_knowledge_content()
    print(f"Found {len(content.data)} content items")

    for item in content.data:
        print(f"  {item.id}: {item.name} ({item.status})")
```

Supports pagination via `limit` and `page` parameters, and sorting via `sort_by` and `sort_order`.

### Update Content Metadata

```python
updated = await client.update_content(
    content_id="content-id-here",
    name="Updated Name",
    description="Updated description",
)
```

### Delete All Content

```python
await client.delete_all_content()
```

### Full Upload and Search Workflow

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

- **Don't write custom Python for basic operations** — use the CLI script for listing, uploading, searching, status checks, and deleting
- **Don't forget `contents_db=` on Knowledge** — required for upload/management endpoints
- **Don't forget `knowledge=[...]` on AgentOS** — registers knowledge API endpoints
- **Don't assume instant processing** — content is processed asynchronously; check status
- **Don't skip error handling** — knowledge endpoints may not be configured on all instances

## Further Reading

For advanced knowledge API patterns, read `references/api-patterns.md`.
