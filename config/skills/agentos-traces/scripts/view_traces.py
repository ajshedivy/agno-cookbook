"""
View execution traces via AgentOSClient.

Prerequisites:
1. Start an AgentOS server with tracing=True
2. Run some agent requests first
3. Run this script: python view_traces.py
"""

import asyncio

from agno.client import AgentOSClient


async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    # List traces
    print("1. Listing traces...")
    traces = await client.list_traces()
    print(f"   Found {len(traces.data)} traces")

    for trace in traces.data[:5]:
        print(f"\n   Trace: {trace.trace_id}")
        print(f"   Agent: {trace.agent_id}")
        print(f"   Created: {trace.created_at}")

        # Get detail
        detail = await client.get_trace(trace.trace_id)
        if hasattr(detail, "spans") and detail.spans:
            for span in detail.spans:
                print(f"     Span: {span.name} ({span.duration_ms}ms)")

    # Stats by session
    print("\n2. Trace stats by session...")
    try:
        stats = await client.get_trace_stats_by_session()
        for entry in stats.data[:5]:
            print(f"   Session: {entry.session_id}")
            print(f"     Traces: {entry.total_traces}")
    except Exception as e:
        print(f"   Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
