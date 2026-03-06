#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["agno[os]"]
# ///
"""
Manage knowledge base content on an AgentOS instance.

Examples:
    # List all content in the knowledge base
    uv run manage_knowledge.py

    # Search the knowledge base
    uv run manage_knowledge.py --search "What is Agno?"

    # Upload a text file (e.g., upload this md file to my knowledge base)
    uv run manage_knowledge.py --upload README.md

    # Upload raw text
    uv run manage_knowledge.py --upload-text "Agno is an AI agent framework" --name "Agno Intro"

    # Check processing status of uploaded content
    uv run manage_knowledge.py --status content-id-123

    # Delete specific content
    uv run manage_knowledge.py --delete content-id-123

    # Use a different server
    uv run manage_knowledge.py --base-url http://my-server:8000
"""

import argparse
import asyncio
import sys
from pathlib import Path

from agno.client import AgentOSClient


async def list_content(client: AgentOSClient) -> None:
    content = await client.list_knowledge_content()
    if not content.data:
        print("No content in knowledge base")
        return

    print(f"Found {len(content.data)} content item(s):\n")
    for item in content.data:
        name = getattr(item, "name", "Unnamed")
        status = getattr(item, "status", "unknown")
        content_type = getattr(item, "type", "unknown")
        print(f"  [{item.id}]")
        print(f"    name: {name}")
        print(f"    type: {content_type} | status: {status}")
        print()


async def search_knowledge(client: AgentOSClient, query: str, limit: int) -> None:
    results = await client.search_knowledge(query=query, limit=limit)
    if not results.data:
        print(f"No results for: {query}")
        return

    print(f"Found {len(results.data)} result(s) for '{query}':\n")
    for result in results.data:
        score = getattr(result, "score", "N/A")
        content = str(getattr(result, "content", ""))
        preview = (content[:200] + "...") if len(content) > 200 else content
        print(f"  [score: {score}]")
        print(f"    {preview}")
        print()


async def upload_file(client: AgentOSClient, file_path: str, name: str | None) -> None:
    path = Path(file_path)
    if not path.exists():
        print(f"File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    text_content = path.read_text()
    content_name = name or path.name

    result = await client.upload_knowledge_content(
        text_content=text_content,
        name=content_name,
        description=f"Uploaded from {path.name}",
    )
    print(f"Uploaded: {result.id}")
    print(f"  name: {content_name}")
    print(f"  status: {result.status}")


async def upload_text(client: AgentOSClient, text: str, name: str) -> None:
    result = await client.upload_knowledge_content(
        text_content=text,
        name=name,
    )
    print(f"Uploaded: {result.id}")
    print(f"  name: {name}")
    print(f"  status: {result.status}")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Manage knowledge base via AgentOS API")
    parser.add_argument("--base-url", default="http://localhost:7777", help="AgentOS server URL (default: http://localhost:7777)")
    parser.add_argument("--search", metavar="QUERY", help="Search the knowledge base")
    parser.add_argument("--limit", type=int, default=5, help="Max search results (default: 5)")
    parser.add_argument("--upload", metavar="FILE", help="Upload a text file to the knowledge base")
    parser.add_argument("--upload-text", metavar="TEXT", help="Upload raw text content")
    parser.add_argument("--name", help="Name for uploaded content")
    parser.add_argument("--status", metavar="CONTENT_ID", help="Check processing status of content")
    parser.add_argument("--delete", metavar="CONTENT_ID", help="Delete specific content by ID")
    args = parser.parse_args()

    client = AgentOSClient(base_url=args.base_url)

    if args.search:
        await search_knowledge(client, args.search, args.limit)
    elif args.upload:
        await upload_file(client, args.upload, args.name)
    elif args.upload_text:
        name = args.name or "Uploaded text"
        await upload_text(client, args.upload_text, name)
    elif args.status:
        status = await client.get_content_status(args.status)
        print(f"Content {args.status}:")
        print(f"  status: {status.status}")
        print(f"  message: {status.status_message}")
    elif args.delete:
        await client.delete_content(args.delete)
        print(f"Deleted content: {args.delete}")
    else:
        await list_content(client)


if __name__ == "__main__":
    asyncio.run(main())
