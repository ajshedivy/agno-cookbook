"""
Memory operations via AgentOSClient.

Prerequisites:
1. Start an AgentOS server with memory enabled (update_memory_on_run=True)
2. Run this script: python manage_memories.py
"""

import asyncio

from agno.client import AgentOSClient


async def main():
    client = AgentOSClient(base_url="http://localhost:7777")
    user_id = "example-user"

    # Create
    print("1. Creating memory...")
    memory = await client.create_memory(
        memory="User prefers dark mode",
        user_id=user_id,
        topics=["preferences", "ui"],
    )
    print(f"   ID: {memory.memory_id}")

    # List
    print("\n2. Listing memories...")
    memories = await client.list_memories(user_id=user_id)
    for mem in memories.data:
        print(f"   {mem.memory_id}: {mem.memory}")

    # Update
    print("\n3. Updating memory...")
    updated = await client.update_memory(
        memory_id=memory.memory_id,
        memory="User strongly prefers dark mode",
        user_id=user_id,
        topics=["preferences", "ui", "accessibility"],
    )
    print(f"   Updated: {updated.memory}")

    # Delete
    print("\n4. Deleting memory...")
    await client.delete_memory(memory.memory_id, user_id=user_id)
    print("   Done")

    # Verify
    memories = await client.list_memories(user_id=user_id)
    print(f"\n   Remaining: {len(memories.data)}")


if __name__ == "__main__":
    asyncio.run(main())
