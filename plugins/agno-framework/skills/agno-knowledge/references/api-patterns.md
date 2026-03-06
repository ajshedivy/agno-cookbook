# Knowledge API Patterns

## Full Knowledge Constructor

```python
Knowledge(
    vector_db=ChromaDb(...),           # Required: vector database
    max_results=5,                     # Max docs per search
    contents_db=SqliteDb(...),         # Track loaded content
    chunking=FixedChunking(...),       # Chunking strategy
)
```

## Vector Database Options

| Backend | Import | Extras |
|---------|--------|--------|
| ChromaDB | `agno.vectordb.chroma.ChromaDb` | `agno[chromadb]` |
| PgVector | `agno.vectordb.pgvector.PgVector` | `agno[pgvector]` |
| LanceDB | `agno.vectordb.lancedb.LanceDb` | `agno[lancedb]` |
| Pinecone | `agno.vectordb.pinecone.Pinecone` | `agno[pinecone]` |
| Qdrant | `agno.vectordb.qdrant.Qdrant` | `agno[qdrant]` |
| Weaviate | `agno.vectordb.weaviate.Weaviate` | `agno[weaviate]` |
| Milvus | `agno.vectordb.milvus.Milvus` | `agno[milvusdb]` |
| Redis | `agno.vectordb.redis.RedisVectorDb` | `agno[redis]` |

## Embedder Options

| Provider | Import | Extras |
|----------|--------|--------|
| Google | `agno.knowledge.embedder.google.GeminiEmbedder` | `agno[google]` |
| OpenAI | `agno.knowledge.embedder.openai.OpenAIEmbedder` | `agno[openai]` |
| Ollama | `agno.knowledge.embedder.ollama.OllamaEmbedder` | `agno[ollama]` |
| Cohere | `agno.knowledge.embedder.cohere.CohereEmbedder` | `agno[cohere]` |

## Reader Options

| Format | Import | Extras |
|--------|--------|--------|
| PDF | `agno.knowledge.reader.pdf.PDFReader` | `agno[pdf]` |
| DOCX | `agno.knowledge.reader.docx.DocxReader` | `agno[docx]` |
| CSV | `agno.knowledge.reader.csv.CSVReader` | `agno[csv]` |
| Text | `agno.knowledge.reader.text.TextReader` | (base) |
| JSON | `agno.knowledge.reader.json.JSONReader` | (base) |

## Chunking Options

```python
from agno.knowledge.chunking.fixed import FixedChunking
from agno.knowledge.chunking.semantic import SemanticChunking
from agno.knowledge.chunking.recursive import RecursiveChunking

FixedChunking(chunk_size=500, overlap=50)
SemanticChunking()
RecursiveChunking(chunk_size=1000, overlap=100)
```

## Search Filtering

```python
from agno.vectordb.search import SearchType

# Filter results by metadata
results = knowledge.search(
    query="deployment guide",
    search_type=SearchType.hybrid,
    filters={"source": "docs"},
)
```

## Loading Content Patterns

```python
# Single URL
knowledge.insert(url="https://example.com/doc.md", skip_if_exists=True)

# Single file
knowledge.insert(path="data/report.pdf", reader=PDFReader(), skip_if_exists=True)

# Directory of files
knowledge.insert(path="data/", reader=PDFReader(), skip_if_exists=True)

# Named content
knowledge.insert(name="Q1 Report", path="q1.pdf", reader=PDFReader())
```

## Custom Retriever

```python
from agno.knowledge.retriever import BaseRetriever

class MyRetriever(BaseRetriever):
    def retrieve(self, query: str, max_results: int = 5):
        # Custom retrieval logic
        return [{"content": "...", "metadata": {...}}]

knowledge = Knowledge(
    retriever=MyRetriever(),
    max_results=5,
)
```
