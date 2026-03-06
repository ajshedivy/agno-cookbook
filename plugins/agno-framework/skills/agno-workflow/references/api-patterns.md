# Agno Workflow API Reference

## Full Workflow Constructor

```python
from agno.workflow.workflow import Workflow
from agno.workflow.step import Step

Workflow(
    name="Workflow Name",
    id="unique-id",
    description="What this workflow does",
    steps=[step1, step2, step3],
    db=SqliteDb(db_file="workflow.db"),
    add_workflow_history_to_steps=True,   # Feed prior outputs to next step
)
```

## Step Constructor

```python
Step(
    name="Step Name",
    agent=my_agent,
    description="What this step does",
)
```

## Common Workflow Patterns

### Content Pipeline
```python
researcher = Agent(name="Researcher", instructions="Gather facts")
writer = Agent(name="Writer", instructions="Write article")
editor = Agent(name="Editor", instructions="Edit for clarity and accuracy")

workflow = Workflow(
    name="Content Pipeline",
    steps=[
        Step(name="Research", agent=researcher),
        Step(name="Write", agent=writer),
        Step(name="Edit", agent=editor),
    ],
)
```

### Data Processing
```python
extractor = Agent(name="Extractor", instructions="Extract structured data")
validator = Agent(name="Validator", instructions="Validate data quality")
loader = Agent(name="Loader", instructions="Format for storage")

workflow = Workflow(
    name="ETL Pipeline",
    steps=[
        Step(name="Extract", agent=extractor),
        Step(name="Validate", agent=validator),
        Step(name="Load", agent=loader),
    ],
)
```

### With Shared Storage
```python
from agno.db.sqlite import SqliteDb

db = SqliteDb(db_file="tmp/workflow.db")

# All agents share the same DB for context
step1_agent = Agent(name="Step 1", db=db, add_history_to_context=True, num_history_runs=5)
step2_agent = Agent(name="Step 2", db=db, add_history_to_context=True, num_history_runs=5)

workflow = Workflow(
    name="Shared State Workflow",
    db=db,
    steps=[
        Step(name="Step 1", agent=step1_agent),
        Step(name="Step 2", agent=step2_agent),
    ],
    add_workflow_history_to_steps=True,
)
```

## Imports Summary

```python
from agno.workflow import Step, Workflow
# OR
from agno.workflow.workflow import Workflow
from agno.workflow.step import Step
```
