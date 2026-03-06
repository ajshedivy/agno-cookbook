---
name: agno-workflow
description: |
  Build step-based workflows with Agno for sequential agent pipelines.
  Trigger this skill when: importing agno.workflow, creating Workflow or
  Step instances, building pipelines, chaining agents, or asking "how do
  I build a workflow with Agno?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["workflow", "pipeline", "agno", "orchestration"]
---

# Build Agno Workflows

Use `agno.workflow.Workflow` and `agno.workflow.Step` to chain agents into sequential pipelines. Install with `pip install agno`.

## Quick Start

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.db.sqlite import SqliteDb
from agno.workflow import Step, Workflow

db = SqliteDb(db_file="tmp/agents.db")

# Step 1: Gather data
data_agent = Agent(
    name="Data Gatherer",
    model=Claude(id="claude-sonnet-4-5"),
    instructions="Fetch comprehensive data. Don't analyze -- just gather and organize.",
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
)

# Step 2: Analyze
analyst = Agent(
    name="Analyst",
    model=Claude(id="claude-sonnet-4-5"),
    instructions="Interpret the data. Identify strengths, weaknesses, and benchmarks.",
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
)

# Step 3: Write report
writer = Agent(
    name="Report Writer",
    model=Claude(id="claude-sonnet-4-5"),
    instructions="Synthesize into a concise brief. Lead with a one-line summary.",
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# Create workflow
workflow = Workflow(
    name="Research Pipeline",
    description="Data -> Analysis -> Report",
    steps=[
        Step(name="Data Gathering", agent=data_agent, description="Fetch data"),
        Step(name="Analysis", agent=analyst, description="Analyze data"),
        Step(name="Report", agent=writer, description="Write report"),
    ],
)

workflow.print_response("Analyze NVIDIA for investment", stream=True)
```

## Step Configuration

Each `Step` wraps an agent with metadata about its role in the pipeline:

```python
from agno.workflow import Step

step = Step(
    name="Step Name",                    # Display name
    agent=my_agent,                      # Agent that handles this step
    description="What this step does",   # Used for routing and documentation
)
```

## Workflow Parameters

```python
from agno.workflow import Workflow

Workflow(
    name="Workflow Name",
    id="unique-id",                       # Auto-generated if omitted
    description="What this workflow does",
    steps=[step1, step2, step3],          # Ordered list of steps
    db=SqliteDb(db_file="workflow.db"),   # Storage backend
    add_workflow_history_to_steps=True,   # Pass prior step outputs to next step
)
```

## Running Workflows

```python
# Sync
workflow.print_response("input prompt", stream=True)
response = workflow.run("input prompt")

# Async
await workflow.aprint_response("input prompt", stream=True)
response = await workflow.arun("input prompt")
```

## Workflow vs Team

| Feature | Workflow | Team |
|---------|----------|------|
| Execution | Sequential steps, predictable order | Dynamic, leader decides |
| Data flow | Output of step N feeds step N+1 | Leader synthesizes |
| Best for | Pipelines, ETL, structured processes | Collaboration, debate |
| Control | Explicit, repeatable | Flexible, adaptive |

**Use Workflow when:**
- Steps must happen in a specific order
- Each step has a clear, specialized role
- You want predictable, repeatable execution
- Output from step N feeds into step N+1

**Use Team when:**
- Agents need to collaborate dynamically
- The leader should decide who to involve
- Tasks benefit from back-and-forth discussion

## Anti-Patterns

- **Don't use workflows for simple tasks** — a single agent is faster
- **Don't skip `add_workflow_history_to_steps=True`** if later steps need context from earlier ones
- **Don't give every step the same instructions** — each step should have a distinct, specialized role
- **Don't make pipelines too deep** — 3-5 steps is ideal; more creates latency

## Further Reading

For advanced workflow features (parallel steps, conditional routing), read `references/api-patterns.md`.
