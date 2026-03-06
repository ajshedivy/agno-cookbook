#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["agno[os]"]
# ///
"""
Manage user memories on an AgentOS instance.

Examples:
    # List all memories for a user
    uv run manage_memories.py --user-id alice@example.com

    # Search memories by content
    uv run manage_memories.py --user-id alice --search "dark mode"

    # Create a new memory
    uv run manage_memories.py --user-id alice --create "User prefers dark mode" --topics preferences,ui

    # Update a memory
    uv run manage_memories.py --memory-id abc-123 --user-id alice --update "User strongly prefers dark mode"

    # Delete a memory
    uv run manage_memories.py --memory-id abc-123 --user-id alice --delete

    # List all memory topics
    uv run manage_memories.py --topics-list

    # Use a different server
    uv run manage_memories.py --base-url http://my-server:8000 --user-id alice
"""

import argparse
import asyncio
import sys

from agno.client import AgentOSClient


async def list_memories(
    client: AgentOSClient,
    user_id: str,
    search: str | None,
) -> None:
    kwargs: dict = {"user_id": user_id}
    if search:
        kwargs["search_content"] = search

    memories = await client.list_memories(**kwargs)
    if not memories.data:
        print(f"No memories found for user {user_id}")
        return

    print(f"Found {len(memories.data)} memory/memories for {user_id}:\n")
    for mem in memories.data:
        topics = ", ".join(mem.topics) if mem.topics else "none"
        print(f"  [{mem.memory_id}]")
        print(f"    {mem.memory}")
        print(f"    topics: {topics}")
        print()


async def create_memory(
    client: AgentOSClient,
    user_id: str,
    content: str,
    topics: list[str] | None,
) -> None:
    kwargs: dict = {"memory": content, "user_id": user_id}
    if topics:
        kwargs["topics"] = topics

    memory = await client.create_memory(**kwargs)
    print(f"Created memory: {memory.memory_id}")
    print(f"  content: {memory.memory}")
    if memory.topics:
        print(f"  topics: {', '.join(memory.topics)}")


async def update_memory(
    client: AgentOSClient,
    memory_id: str,
    user_id: str,
    content: str,
    topics: list[str] | None,
) -> None:
    kwargs: dict = {"memory_id": memory_id, "memory": content, "user_id": user_id}
    if topics:
        kwargs["topics"] = topics

    updated = await client.update_memory(**kwargs)
    print(f"Updated memory: {updated.memory_id}")
    print(f"  content: {updated.memory}")
    if updated.topics:
        print(f"  topics: {', '.join(updated.topics)}")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Manage memories via AgentOS API")
    parser.add_argument("--base-url", default="http://localhost:7777", help="AgentOS server URL (default: http://localhost:7777)")
    parser.add_argument("--user-id", help="User ID to scope memories to")
    parser.add_argument("--memory-id", help="Memory ID for get/update/delete")
    parser.add_argument("--search", help="Search memory content (fuzzy match)")
    parser.add_argument("--create", metavar="CONTENT", help="Create a new memory with this content")
    parser.add_argument("--update", metavar="CONTENT", help="Update memory content (requires --memory-id)")
    parser.add_argument("--delete", action="store_true", help="Delete a memory (requires --memory-id)")
    parser.add_argument("--topics", help="Comma-separated topics (for --create or --update)")
    parser.add_argument("--topics-list", action="store_true", help="List all unique memory topics")
    args = parser.parse_args()

    client = AgentOSClient(base_url=args.base_url)
    topic_list = [t.strip() for t in args.topics.split(",")] if args.topics else None

    if args.topics_list:
        topics = await client.get_memory_topics()
        print(f"Memory topics: {topics}")
    elif args.create:
        if not args.user_id:
            print("--create requires --user-id", file=sys.stderr)
            sys.exit(1)
        await create_memory(client, args.user_id, args.create, topic_list)
    elif args.update:
        if not args.memory_id or not args.user_id:
            print("--update requires --memory-id and --user-id", file=sys.stderr)
            sys.exit(1)
        await update_memory(client, args.memory_id, args.user_id, args.update, topic_list)
    elif args.delete:
        if not args.memory_id or not args.user_id:
            print("--delete requires --memory-id and --user-id", file=sys.stderr)
            sys.exit(1)
        await client.delete_memory(args.memory_id, user_id=args.user_id)
        print(f"Deleted memory: {args.memory_id}")
    elif args.memory_id and args.user_id:
        mem = await client.get_memory(args.memory_id, user_id=args.user_id)
        print(f"Memory: {mem.memory_id}")
        print(f"  content: {mem.memory}")
        print(f"  topics: {', '.join(mem.topics) if mem.topics else 'none'}")
    elif args.user_id:
        await list_memories(client, args.user_id, args.search)
    else:
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())
