# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "agno[openai,opentelemetry]",
#     "openinference-instrumentation-agno",
#     "opentelemetry-exporter-otlp-proto-http",
#     "opentelemetry-sdk",
# ]
# ///
"""
Observability Demo
===================
Self-contained demo of OpenTelemetry instrumentation for Agno agents.
Exports traces to a configurable OTLP endpoint (Langfuse, Arize Phoenix, etc.).

Usage:
    # With Langfuse
    export OPENAI_API_KEY=sk-...
    export OTEL_EXPORTER_OTLP_ENDPOINT=https://cloud.langfuse.com/api/public/otel
    export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Basic <base64-encoded-key>"
    uv run observability_demo.py

    # With local Arize Phoenix
    export OPENAI_API_KEY=sk-...
    uv run observability_demo.py --endpoint http://localhost:6006/v1/traces

    # Dry run (no tracing, just agent)
    uv run observability_demo.py --dry-run
"""

import argparse
import os


def setup_tracing(endpoint: str):
    """Configure OpenTelemetry tracing with OTLP exporter."""
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from openinference.instrumentation.agno import AgnoInstrumentor

    provider = TracerProvider()
    provider.add_span_processor(
        SimpleSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
    )
    trace.set_tracer_provider(provider)

    # Instrument Agno — all agent runs will be traced
    AgnoInstrumentor().instrument()
    print(f"Tracing enabled → {endpoint}")


def main():
    parser = argparse.ArgumentParser(description="Observability demo")
    parser.add_argument(
        "--model",
        default="openai:gpt-4o",
        help="Model string, e.g. 'openai:gpt-4o' or 'anthropic:claude-sonnet-4-5'",
    )
    parser.add_argument(
        "--endpoint",
        default=os.environ.get(
            "OTEL_EXPORTER_OTLP_ENDPOINT",
            "http://localhost:6006/v1/traces",
        ),
        help="OTLP endpoint URL",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without tracing (just the agent)",
    )
    args = parser.parse_args()

    # Set up tracing unless dry-run
    if not args.dry_run:
        setup_tracing(args.endpoint)
    else:
        print("Dry run — tracing disabled")

    # Import after instrumentation so spans are captured
    from agno.agent import Agent
    from agno.tools.calculator import CalculatorTools

    agent = Agent(
        name="Traced Agent",
        model=args.model,
        tools=[CalculatorTools()],
        instructions=["You are a helpful assistant. Show your work."],
        markdown=True,
    )

    # Run several interactions to generate traces
    queries = [
        "What is 42 * 17?",
        "Calculate 2^10 and explain what it means.",
        "What is the square root of 144?",
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n{'='*50}")
        print(f"Query {i}: {query}")
        print(f"{'='*50}\n")
        agent.print_response(query, stream=True)

    print("\n\nAll queries complete.")
    if not args.dry_run:
        print(f"View traces at your observability platform: {args.endpoint}")


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
