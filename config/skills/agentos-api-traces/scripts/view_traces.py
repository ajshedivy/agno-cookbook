#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["agno[os]"]
# ///
"""
View and inspect execution traces on an AgentOS instance.

Examples:
    # List recent traces
    uv run view_traces.py

    # Get detailed trace info
    uv run view_traces.py --trace-id abc-123

    # View trace stats grouped by session
    uv run view_traces.py --stats

    # Limit the number of traces shown
    uv run view_traces.py --limit 5

    # Use a different server
    uv run view_traces.py --base-url http://my-server:8000
"""

import argparse
import asyncio

from agno.client import AgentOSClient


async def list_traces(client: AgentOSClient, limit: int) -> None:
    traces = await client.list_traces()
    items = traces.data[:limit] if traces.data else []
    if not items:
        print("No traces found")
        return

    print(f"Showing {len(items)} trace(s):\n")
    for trace in items:
        trace_id = getattr(trace, "trace_id", "N/A")
        agent_id = getattr(trace, "agent_id", "N/A")
        session_id = getattr(trace, "session_id", "N/A")
        created = getattr(trace, "created_at", "")
        print(f"  [{trace_id}]")
        print(f"    agent: {agent_id} | session: {session_id}")
        if created:
            print(f"    created: {created}")
        print()


async def get_trace_detail(client: AgentOSClient, trace_id: str) -> None:
    trace = await client.get_trace(trace_id)
    print(f"Trace: {trace.trace_id}")
    print(f"  agent: {getattr(trace, 'agent_id', 'N/A')}")
    duration = getattr(trace, "duration_ms", None)
    if duration:
        print(f"  duration: {duration}ms")

    spans = getattr(trace, "spans", None) or []
    if spans:
        print(f"\n  Spans ({len(spans)}):")
        for span in spans:
            name = getattr(span, "name", "unnamed")
            span_duration = getattr(span, "duration_ms", "?")
            tokens = getattr(span, "total_tokens", "?")
            print(f"    {name}: {span_duration}ms | tokens: {tokens}")


async def show_trace_stats(client: AgentOSClient) -> None:
    stats = await client.get_trace_stats_by_session()
    if not stats.data:
        print("No trace stats available")
        return

    print(f"Trace stats for {len(stats.data)} session(s):\n")
    for entry in stats.data:
        session_id = getattr(entry, "session_id", "N/A")
        total = getattr(entry, "total_traces", 0)
        first = getattr(entry, "first_trace_at", "")
        last = getattr(entry, "last_trace_at", "")
        print(f"  session: {session_id}")
        print(f"    traces: {total} | first: {first} | last: {last}")
        print()


async def main() -> None:
    parser = argparse.ArgumentParser(description="View traces via AgentOS API")
    parser.add_argument("--base-url", default="http://localhost:7777", help="AgentOS server URL (default: http://localhost:7777)")
    parser.add_argument("--trace-id", help="Get detailed info for a specific trace")
    parser.add_argument("--stats", action="store_true", help="Show trace statistics grouped by session")
    parser.add_argument("--limit", type=int, default=20, help="Max traces to list (default: 20)")
    args = parser.parse_args()

    client = AgentOSClient(base_url=args.base_url)

    if args.trace_id:
        await get_trace_detail(client, args.trace_id)
    elif args.stats:
        await show_trace_stats(client)
    else:
        await list_traces(client, args.limit)


if __name__ == "__main__":
    asyncio.run(main())
