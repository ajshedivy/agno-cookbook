#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["agno[os]"]
# ///
"""
View and inspect execution traces on an AgentOS instance.

Examples:
    # List recent traces
    uv run view_traces.py --base-url http://localhost:8000 --db-id agentos-db

    # Get detailed trace info
    uv run view_traces.py --base-url http://localhost:8000 --db-id agentos-db \
        --trace-id abc-123

    # View trace stats grouped by session
    uv run view_traces.py --base-url http://localhost:8000 --db-id agentos-db --stats

    # Limit the number of traces shown
    uv run view_traces.py --base-url http://localhost:8000 --db-id agentos-db --limit 5

    # Auto-detect db_id from server config
    uv run view_traces.py --base-url http://localhost:8000
"""

import argparse
import asyncio

from agno.client import AgentOSClient


async def resolve_db_id(client: AgentOSClient, db_id: str | None) -> str | None:
    """Resolve db_id: use provided value, auto-detect from config, or None."""
    if db_id:
        return db_id
    try:
        config = await client.aget_config()
        traces_cfg = getattr(config, "traces", None)
        if traces_cfg:
            dbs = getattr(traces_cfg, "dbs", None) or []
            if len(dbs) == 1:
                return getattr(dbs[0], "db_id", None)
            elif len(dbs) > 1:
                db_ids = [getattr(db, "db_id", "?") for db in dbs]
                print(f"Multiple trace databases found: {db_ids}")
                print("Please specify one with --db-id")
                return None
    except Exception:
        pass
    return None


async def list_traces(client: AgentOSClient, limit: int, db_id: str | None) -> None:
    traces = await client.get_traces(limit=limit, db_id=db_id)
    items = traces.data[:limit] if traces.data else []
    if not items:
        print("No traces found")
        return

    print(f"Showing {len(items)} trace(s):\n")
    for trace in items:
        print(f"  [{trace.trace_id}]")
        print(f"    name: {trace.name}")
        print(f"    agent: {trace.agent_id or 'N/A'} | session: {trace.session_id or 'N/A'}")
        print(f"    status: {trace.status} | duration: {trace.duration} | spans: {trace.total_spans} | errors: {trace.error_count}")
        if trace.created_at:
            print(f"    created: {trace.created_at}")
        if trace.input:
            truncated = trace.input[:120] + "..." if len(trace.input) > 120 else trace.input
            print(f"    input: {truncated}")
        print()


async def get_trace_detail(client: AgentOSClient, trace_id: str, db_id: str | None) -> None:
    trace = await client.get_trace(trace_id, db_id=db_id)
    print(f"Trace: {trace.trace_id}")
    print(f"  name: {trace.name}")
    print(f"  agent: {trace.agent_id or 'N/A'}")
    print(f"  status: {trace.status} | duration: {trace.duration}")
    print(f"  spans: {trace.total_spans} | errors: {trace.error_count}")
    if trace.run_id:
        print(f"  run_id: {trace.run_id}")
    if trace.session_id:
        print(f"  session: {trace.session_id}")

    tree = getattr(trace, "tree", None) or []
    if tree:
        print(f"\n  Span Tree ({len(tree)} root node(s)):")
        _print_span_tree(tree, indent=4)


def _print_span_tree(nodes: list, indent: int = 4) -> None:
    prefix = " " * indent
    for node in nodes:
        name = getattr(node, "name", "unnamed")
        node_type = getattr(node, "type", "?")
        duration = getattr(node, "duration", "?")
        status = getattr(node, "status", "?")
        print(f"{prefix}{name} ({node_type}) [{status}] {duration}")
        children = getattr(node, "spans", None) or []
        if children:
            _print_span_tree(children, indent + 4)


async def show_trace_stats(client: AgentOSClient, db_id: str | None) -> None:
    stats = await client.get_trace_session_stats(db_id=db_id)
    if not stats.data:
        print("No trace stats available")
        return

    print(f"Trace stats for {len(stats.data)} session(s):\n")
    for entry in stats.data:
        print(f"  session: {entry.session_id}")
        print(f"    agent: {entry.agent_id or 'N/A'} | traces: {entry.total_traces}")
        print(f"    first: {entry.first_trace_at} | last: {entry.last_trace_at}")
        print()


async def main() -> None:
    parser = argparse.ArgumentParser(description="View traces via AgentOS API")
    parser.add_argument("--base-url", default="http://localhost:7777", help="AgentOS server URL (default: http://localhost:7777)")
    parser.add_argument("--db-id", default=None, help="Database ID for traces (auto-detected if only one exists)")
    parser.add_argument("--trace-id", help="Get detailed info for a specific trace")
    parser.add_argument("--stats", action="store_true", help="Show trace statistics grouped by session")
    parser.add_argument("--limit", type=int, default=20, help="Max traces to list (default: 20)")
    args = parser.parse_args()

    client = AgentOSClient(base_url=args.base_url)
    db_id = await resolve_db_id(client, args.db_id)

    if args.trace_id:
        await get_trace_detail(client, args.trace_id, db_id)
    elif args.stats:
        await show_trace_stats(client, db_id)
    else:
        await list_traces(client, args.limit, db_id)


if __name__ == "__main__":
    asyncio.run(main())
