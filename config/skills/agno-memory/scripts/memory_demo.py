# /// script
# requires-python = ">=3.11"
# dependencies = ["agno[openai]"]
# ///
"""
Memory Demo
============
Self-contained demo of agent memory — user preferences that persist across
sessions.

Usage:
    export OPENAI_API_KEY=sk-...
    uv run memory_demo.py
    uv run memory_demo.py --model "anthropic:claude-sonnet-4-5"
    uv run memory_demo.py --user "alice@example.com"
"""

import argparse

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
TMP_DIR = "tmp/memory_demo"


def main():
    parser = argparse.ArgumentParser(description="Agent memory demo")
    parser.add_argument(
        "--model",
        default="openai:gpt-4o",
        help="Model string, e.g. 'openai:gpt-4o' or 'anthropic:claude-sonnet-4-5'",
    )
    parser.add_argument(
        "--user",
        default="demo-user",
        help="User ID for memory isolation",
    )
    args = parser.parse_args()

    db = SqliteDb(db_file=f"{TMP_DIR}/agents.db")

    # Memory manager extracts and stores user-level facts
    memory_manager = MemoryManager(
        model=args.model,
        db=db,
        additional_instructions=[
            "Capture the user's preferences and interests.",
            "Remember technical context (languages, frameworks, tools).",
            "Ignore greetings and small talk.",
        ],
    )

    agent = Agent(
        name="Memory Agent",
        model=args.model,
        db=db,
        memory_manager=memory_manager,
        enable_agentic_memory=True,
        add_history_to_context=True,
        num_history_runs=5,
        instructions=[
            "You are a helpful assistant that remembers user preferences.",
            "Reference what you know about the user when relevant.",
        ],
        markdown=True,
    )

    # --- Conversation 1: Store preferences ---
    print("=== Conversation 1: Storing preferences ===\n")
    agent.print_response(
        "I'm a Python developer and I prefer dark mode in all my editors.",
        user_id=args.user,
        session_id="session-1",
        stream=True,
    )

    print("\n\n=== Conversation 2: Store more context ===\n")
    agent.print_response(
        "I'm working on a project called Orion that uses FastAPI and PostgreSQL.",
        user_id=args.user,
        session_id="session-2",
        stream=True,
    )

    # --- Check stored memories ---
    print("\n\n=== Stored Memories ===\n")
    memories = agent.get_user_memories(user_id=args.user)
    if memories:
        for i, m in enumerate(memories, 1):
            print(f"  {i}. {m.memory}")
    else:
        print("  (no memories stored yet)")

    # --- Conversation 3: Recall in a new session ---
    print("\n\n=== Conversation 3: Recalling in new session ===\n")
    agent.print_response(
        "What do you know about me and my work?",
        user_id=args.user,
        session_id="session-3",
        stream=True,
    )


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
