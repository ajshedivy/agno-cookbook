---
name: agno-knowledge
description: |
  Build knowledge bases for Agno agents using vector databases, embedders,
  and document readers. Covers ChromaDB, PgVector, LanceDB, document loading,
  chunking strategies, and hybrid search. Trigger this skill when: importing
  agno.knowledge, creating Knowledge instances, adding documents to agents,
  configuring vector databases, or asking "how do I add a knowledge base?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["knowledge", "rag", "vector-db", "embeddings", "agno"]
---

# Build Agno Knowledge Bases

Use `agno.knowledge.knowledge.Knowledge` with a vector database to give agents searchable document collections. Install with `pip install agno`.

## Quick Start

```python
from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.search import SearchType

knowledge = Knowledge(
    vector_db=ChromaDb(
        collection="docs",
        path="tmp/chromadb",
        persistent_client=True,
        search_type=SearchType.hybrid,
        embedder=GeminiEmbedder(id="gemini-embedding-001"),
    ),
)

# Load content
knowledge.insert(url="https://docs.agno.com/introduction.md", skip_if_exists=True)

agent = Agent(
    model="openai:gpt-4o",
    knowledge=knowledge,
    search_knowledge=True,
    markdown=True,
)

agent.print_response("What is Agno?", stream=True)
```

## Core Knowledge Parameters

```python
Knowledge(
    vector_db=ChromaDb(...),      # Required: vector database backend
    max_results=5,                # Max documents returned per search
    contents_db=SqliteDb(...),    # Optional: track loaded content
)
```

## Vector Database Backends

### ChromaDB (Local, no server needed)

```python
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.vectordb.search import SearchType

vector_db = ChromaDb(
    collection="my_docs",
    path="tmp/chromadb",
    persistent_client=True,
    search_type=SearchType.hybrid,
    embedder=GeminiEmbedder(id="gemini-embedding-001"),
)
```

### PgVector (PostgreSQL)

```python
from agno.vectordb.pgvector import PgVector
from agno.knowledge.embedder.openai import OpenAIEmbedder

vector_db = PgVector(
    table_name="documents",
    db_url="postgresql+psycopg://user:pass@localhost:5432/mydb",
    search_type=SearchType.hybrid,
    embedder=OpenAIEmbedder(id="text-embedding-3-small"),
)
```

### LanceDB (Local, columnar)

```python
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.embedder.google import GeminiEmbedder

vector_db = LanceDb(
    uri="tmp/lancedb",
    table_name="documents",
    embedder=GeminiEmbedder(id="gemini-embedding-001"),
)
```

## Embedders

```python
# Google
from agno.knowledge.embedder.google import GeminiEmbedder
embedder = GeminiEmbedder(id="gemini-embedding-001")

# OpenAI
from agno.knowledge.embedder.openai import OpenAIEmbedder
embedder = OpenAIEmbedder(id="text-embedding-3-small")

# Ollama (local)
from agno.knowledge.embedder.ollama import OllamaEmbedder
embedder = OllamaEmbedder(id="nomic-embed-text")
```

## Loading Documents

### From URLs

```python
knowledge.insert(url="https://example.com/doc.md", skip_if_exists=True)
```

### From Local Files (PDF, DOCX, Text)

```python
from agno.knowledge.reader.pdf import PDFReader
from agno.knowledge.reader.docx import DocxReader
from agno.knowledge.reader.text import TextReader

# PDF
knowledge.insert(
    path="docs/report.pdf",
    reader=PDFReader(),
    skip_if_exists=True,
)

# DOCX
knowledge.insert(
    path="docs/spec.docx",
    reader=DocxReader(),
    skip_if_exists=True,
)

# Plain text / markdown
knowledge.insert(
    path="docs/readme.md",
    reader=TextReader(),
    skip_if_exists=True,
)
```

### From Directories

```python
knowledge.insert(
    path="docs/",
    reader=PDFReader(),
    skip_if_exists=True,
)
```

## Search Types

```python
from agno.vectordb.search import SearchType

# Semantic similarity (default)
SearchType.vector

# Keyword-based
SearchType.keyword

# Combined semantic + keyword
SearchType.hybrid
```

## Chunking

Control how documents are split into searchable chunks:

```python
from agno.knowledge.chunking.fixed import FixedChunking
from agno.knowledge.chunking.semantic import SemanticChunking

# Fixed-size chunks
knowledge = Knowledge(
    vector_db=vector_db,
    chunking=FixedChunking(chunk_size=500, overlap=50),
)

# Semantic chunking (splits at natural boundaries)
knowledge = Knowledge(
    vector_db=vector_db,
    chunking=SemanticChunking(),
)
```

## Knowledge with Content Tracking

Track which documents have been loaded to avoid re-processing:

```python
from agno.db.sqlite import SqliteDb

db = SqliteDb(db_file="tmp/agents.db")

knowledge = Knowledge(
    vector_db=vector_db,
    contents_db=db,
    max_results=5,
)
```

## Agent with Knowledge

```python
agent = Agent(
    model="openai:gpt-4o",
    knowledge=knowledge,
    search_knowledge=True,       # Agent searches automatically
    # OR
    # search_knowledge=False,    # Agent uses knowledge tools manually
    markdown=True,
)
```

## Knowledge Tools

Give agents explicit control over knowledge search:

```python
from agno.tools.knowledge import KnowledgeTools

agent = Agent(
    model="openai:gpt-4o",
    knowledge=knowledge,
    tools=[KnowledgeTools()],
    search_knowledge=False,  # Let the agent decide when to search
)
```

## Anti-Patterns

- **Don't skip `skip_if_exists=True`** on insert — you'll re-index documents on every run
- **Don't forget an embedder** — the vector DB needs one to generate embeddings
- **Don't use `SearchType.keyword` alone** — hybrid gives better results in most cases
- **Don't load huge documents without chunking** — they won't fit in context windows
- **Don't hardcode embedder models** — match the embedder to your deployment constraints

## Further Reading

For advanced knowledge patterns, custom retrievers, and cloud storage, read `references/api-patterns.md`.
