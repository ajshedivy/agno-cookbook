# /// script
# requires-python = ">=3.11"
# dependencies = ["agno[openai,chromadb]", "chromadb"]
# ///
"""
Knowledge Base Demo
====================
Self-contained demo of building a knowledge base with ChromaDB and querying
it via an Agno agent.

Usage:
    export OPENAI_API_KEY=sk-...
    uv run knowledge_demo.py
    uv run knowledge_demo.py --model "anthropic:claude-sonnet-4-5"
    uv run knowledge_demo.py --query "What is Agno?"
"""

import argparse
import shutil

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.search import SearchType

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
TMP_DIR = "tmp/knowledge_demo"


def build_knowledge(db: SqliteDb) -> Knowledge:
    """Create a knowledge base backed by ChromaDB with hybrid search."""
    return Knowledge(
        vector_db=ChromaDb(
            collection="demo_docs",
            path=f"{TMP_DIR}/chromadb",
            persistent_client=True,
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-small"),
        ),
        contents_db=db,
        max_results=5,
    )


def main():
    parser = argparse.ArgumentParser(description="Knowledge base demo")
    parser.add_argument(
        "--model",
        default="openai:gpt-4o",
        help="Model string, e.g. 'openai:gpt-4o' or 'anthropic:claude-sonnet-4-5'",
    )
    parser.add_argument(
        "--query",
        default="What is Agno and what can it do?",
        help="Question to ask the knowledge base",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete existing data and re-index",
    )
    args = parser.parse_args()

    if args.clean:
        shutil.rmtree(TMP_DIR, ignore_errors=True)

    db = SqliteDb(db_file=f"{TMP_DIR}/agents.db")
    knowledge = build_knowledge(db)

    # Load a document into the knowledge base
    print("Loading documents into knowledge base...")
    knowledge.insert(
        url="https://docs.agno.com/introduction.md",
        skip_if_exists=True,
    )
    print("Documents loaded.\n")

    # Build an agent that searches the knowledge base
    agent = Agent(
        name="Knowledge Agent",
        model=args.model,
        knowledge=knowledge,
        search_knowledge=True,
        instructions=[
            "Always cite which document your answer comes from.",
            "If the knowledge base doesn't have the answer, say so.",
        ],
        markdown=True,
    )

    # Ask a question
    print(f"Question: {args.query}\n")
    agent.print_response(args.query, stream=True)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
