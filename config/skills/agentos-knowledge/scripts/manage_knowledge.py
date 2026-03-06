"""
Knowledge base operations via AgentOSClient.

Prerequisites:
1. Start an AgentOS server with knowledge configured
2. Run this script: python manage_knowledge.py
"""

import asyncio

from agno.client import AgentOSClient


async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    # Upload content
    print("1. Uploading content...")
    try:
        result = await client.upload_knowledge_content(
            text_content="Agno is a framework for building AI agents and teams.",
            name="Agno Overview",
            description="Overview of the Agno framework",
        )
        print(f"   Content ID: {result.id}")
        print(f"   Status: {result.status}")

        # Check status
        print("\n2. Checking status...")
        status = await client.get_content_status(result.id)
        print(f"   Status: {status.status}")
    except Exception as e:
        print(f"   Error: {e}")

    # List content
    print("\n3. Listing content...")
    try:
        content = await client.list_knowledge_content()
        for item in content.data:
            print(f"   {item.id}: {item.name} ({item.status})")
    except Exception as e:
        print(f"   Error: {e}")

    # Search
    print("\n4. Searching knowledge base...")
    try:
        results = await client.search_knowledge(query="What is Agno?", limit=5)
        for r in results.data:
            preview = str(r.content)[:100] if hasattr(r, "content") else "N/A"
            print(f"   {preview}...")
    except Exception as e:
        print(f"   Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
