# Agno Team API Reference

## Team Modes

```python
from agno.team.mode import TeamMode

# Coordinate (default): Leader selects agents, crafts tasks, synthesizes
TeamMode.coordinate

# Route: Leader routes to single specialist, returns their response directly
TeamMode.route

# Broadcast: Sends request to ALL members simultaneously
TeamMode.broadcast
```

## Full Team Constructor

```python
from agno.team.team import Team

Team(
    name="Team Name",
    id="unique-id",                            # Auto-generated if omitted
    model=Claude(id="claude-sonnet-4-5"),      # Leader model
    members=[agent1, agent2],                   # List of Agent instances
    mode=TeamMode.coordinate,                   # Coordination strategy
    instructions=["How to coordinate."],        # Leader instructions
    description="What this team does",          # Used for nested team routing

    # Display
    show_members_responses=True,
    markdown=True,

    # Storage
    db=SqliteDb(db_file="team.db"),
    add_history_to_context=True,
    num_history_runs=5,
    enable_session_summaries=True,

    # Memory
    update_memory_on_run=True,

    # Context
    add_datetime_to_context=True,
)
```

## Running Teams

```python
# Sync
team.print_response("prompt", stream=True)
response = team.run("prompt")
response = team.run("prompt", session_id="session-1")

# Async
await team.aprint_response("prompt", stream=True)
response = await team.arun("prompt")
```

## Common Team Patterns

### Research + Analysis Pipeline
```python
researcher = Agent(name="Researcher", role="Gather information", tools=[WebSearchTools()])
analyst = Agent(name="Analyst", role="Analyze data", tools=[CalculatorTools()])
writer = Agent(name="Writer", role="Write reports")

team = Team(
    name="Research Pipeline",
    mode=TeamMode.coordinate,
    members=[researcher, analyst, writer],
    instructions=["Research first, analyze second, write last."],
)
```

### Specialist Router
```python
code_agent = Agent(name="Coder", role="Write and debug code")
docs_agent = Agent(name="Docs", role="Write documentation")
test_agent = Agent(name="Tester", role="Write tests")

team = Team(
    name="Dev Router",
    mode=TeamMode.route,
    members=[code_agent, docs_agent, test_agent],
    instructions=["Route coding tasks to Coder, docs to Docs, tests to Tester."],
)
```

### Debate / Adversarial
```python
proponent = Agent(name="Proponent", role="Argue FOR the position")
opponent = Agent(name="Opponent", role="Argue AGAINST the position")

team = Team(
    name="Debate Team",
    mode=TeamMode.coordinate,
    members=[proponent, opponent],
    instructions=["Get both perspectives, then synthesize a balanced conclusion."],
)
```
