# /// script
# requires-python = ">=3.11"
# dependencies = ["agno[openai]"]
# ///
"""
Storage Demo
=============
Self-contained demo of persistent storage — conversation history that
survives across script runs.

Usage:
    export OPENAI_API_KEY=sk-...
    uv run storage_demo.py
    uv run storage_demo.py --model "anthropic:claude-sonnet-4-5"
    uv run storage_demo.py --session "my-session"
"""

import argparse

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.run import RunContext

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
TMP_DIR = "tmp/storage_demo"


# ---------------------------------------------------------------------------
# Custom tool using session state
# ---------------------------------------------------------------------------
def add_to_list(run_context: RunContext, item: str) -> str:
    """Add an item to the shopping list."""
    items = run_context.session_state.get("items", [])
    items.append(item)
    run_context.session_state["items"] = items
    return f"Added '{item}'. List now has {len(items)} item(s): {', '.join(items)}"


def show_list(run_context: RunContext) -> str:
    """Show all items in the shopping list."""
    items = run_context.session_state.get("items", [])
    if not items:
        return "The shopping list is empty."
    return f"Shopping list ({len(items)} items): {', '.join(items)}"


def main():
    parser = argparse.ArgumentParser(description="Storage demo")
    parser.add_argument(
        "--model",
        default="openai:gpt-4o",
        help="Model string, e.g. 'openai:gpt-4o' or 'anthropic:claude-sonnet-4-5'",
    )
    parser.add_argument(
        "--session",
        default="demo-session",
        help="Session ID for conversation continuity",
    )
    args = parser.parse_args()

    db = SqliteDb(db_file=f"{TMP_DIR}/agents.db")

    agent = Agent(
        name="Storage Agent",
        model=args.model,
        db=db,
        tools=[add_to_list, show_list],
        session_state={"items": []},
        add_session_state_to_context=True,
        add_history_to_context=True,
        num_history_runs=5,
        instructions=[
            "You are a shopping assistant.",
            "Help the user manage their shopping list.",
            "Current list: {items}",
        ],
        markdown=True,
    )

    # --- Turn 1: Introduce yourself ---
    print("=== Turn 1: Introduction ===\n")
    agent.print_response(
        "Hi, my name is Alice!",
        session_id=args.session,
        stream=True,
    )

    # --- Turn 2: Add items ---
    print("\n\n=== Turn 2: Add items ===\n")
    agent.print_response(
        "Add milk, eggs, and bread to my shopping list.",
        session_id=args.session,
        stream=True,
    )

    # --- Turn 3: Recall context ---
    print("\n\n=== Turn 3: Recall ===\n")
    agent.print_response(
        "What's my name and what's on my list?",
        session_id=args.session,
        stream=True,
    )

    # --- Show final state ---
    print("\n\n=== Final Session State ===\n")
    state = agent.get_session_state()
    print(f"  Items: {state.get('items', [])}")


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
