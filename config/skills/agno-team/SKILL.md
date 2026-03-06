---
name: agno-team
description: |
  Build multi-agent teams with Agno. Covers coordinate, route, and broadcast
  modes for agent collaboration. Trigger this skill when: importing agno.team,
  creating a Team instance, building multi-agent systems, coordinating
  multiple agents, or asking "how do I build a team with Agno?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["team", "multi-agent", "agno", "coordination"]
---

# Build Agno Teams

Use `agno.team.Team` to coordinate multiple specialized agents. Install with `pip install agno`.

## Quick Start

```python
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.team.team import Team

researcher = Agent(
    name="Researcher",
    role="Research specialist",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["Find and summarize information."],
)

writer = Agent(
    name="Writer",
    role="Content writer",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["Write polished, engaging text."],
)

team = Team(
    name="Research Team",
    model=Claude(id="claude-sonnet-4-5"),
    members=[researcher, writer],
    instructions=["Coordinate research and writing."],
    show_members_responses=True,
    markdown=True,
)

team.print_response("Write an overview of LLM training", stream=True)
```

## Team Modes

Import `TeamMode` to set the coordination strategy:

```python
from agno.team.mode import TeamMode
```

### Coordinate Mode (Default)

The team leader analyzes the request, selects member(s), crafts tasks, and synthesizes responses.

```python
team = Team(
    name="Research Team",
    mode=TeamMode.coordinate,  # Default
    model=Claude(id="claude-sonnet-4-5"),
    members=[researcher, writer],
    instructions=[
        "You lead a research and writing team.",
        "Ask the Researcher to gather facts first,",
        "then ask the Writer to polish into a final piece.",
    ],
    show_members_responses=True,
    markdown=True,
)
```

### Route Mode

Routes each request to a single specialist. No synthesis — the specialist's response is returned directly.

```python
english_agent = Agent(
    name="English Agent",
    role="Responds only in English",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["Always respond in English."],
)

spanish_agent = Agent(
    name="Spanish Agent",
    role="Responds only in Spanish",
    model=Claude(id="claude-sonnet-4-5"),
    instructions=["Always respond in Spanish."],
)

team = Team(
    name="Language Router",
    mode=TeamMode.route,
    model=Claude(id="claude-sonnet-4-5"),
    members=[english_agent, spanish_agent],
    instructions=[
        "Detect the language and route to the matching agent.",
        "Default to English Agent if unsupported.",
    ],
    show_members_responses=True,
    markdown=True,
)
```

### Broadcast Mode

Sends the same request to all members simultaneously. Use for debates, parallel analysis, or multi-perspective research.

```python
bull_analyst = Agent(
    name="Bull Analyst",
    role="Make the case FOR investing",
    model=Claude(id="claude-sonnet-4-5"),
    tools=[YFinanceTools()],
    instructions=["Find the positives: growth drivers, competitive advantages."],
)

bear_analyst = Agent(
    name="Bear Analyst",
    role="Make the case AGAINST investing",
    model=Claude(id="claude-sonnet-4-5"),
    tools=[YFinanceTools()],
    instructions=["Find the risks: valuation concerns, competitive threats."],
)

team = Team(
    name="Investment Research",
    mode=TeamMode.coordinate,
    model=Claude(id="claude-sonnet-4-5"),
    members=[bull_analyst, bear_analyst],
    instructions=[
        "Send the stock to BOTH analysts.",
        "Synthesize into a balanced Buy/Hold/Sell recommendation.",
    ],
    show_members_responses=True,
    markdown=True,
)
```

## Core Team Parameters

```python
Team(
    name="Team Name",
    model=Claude(id="claude-sonnet-4-5"),      # Leader's model
    members=[agent1, agent2],                   # Member agents
    mode=TeamMode.coordinate,                   # coordinate | route | broadcast
    instructions=["Leader instructions."],      # How the leader coordinates
    show_members_responses=True,                # Show individual member outputs
    markdown=True,                              # Format output as markdown

    # Storage (shared across team)
    db=SqliteDb(db_file="tmp/agents.db"),
    add_history_to_context=True,
    num_history_runs=5,

    # Memory
    update_memory_on_run=True,

    # Context
    add_datetime_to_context=True,
)
```

## Agent Roles

Each member agent should have a clear `role` that helps the leader decide when to delegate:

```python
Agent(
    name="Web Agent",
    role="Search the web for current information",  # <-- Key for routing
    model=Claude(id="claude-sonnet-4-5"),
    tools=[WebSearchTools()],
    instructions=["Search the web and provide factual summaries."],
)
```

## Shared Storage

All team members can share the same database for persistent sessions:

```python
from agno.db.sqlite import SqliteDb

team_db = SqliteDb(db_file="tmp/team.db")

agent1 = Agent(name="Agent 1", model=model, db=team_db)
agent2 = Agent(name="Agent 2", model=model, db=team_db)

team = Team(
    name="My Team",
    model=model,
    members=[agent1, agent2],
    db=team_db,
    add_history_to_context=True,
    num_history_runs=5,
)
```

## When to Use Teams vs Single Agents

**Single Agent:**
- One coherent task
- No need for opposing views
- Simpler is better

**Team:**
- Multiple perspectives needed (bull/bear analysis)
- Specialized expertise (web search + data analysis)
- Complex tasks benefiting from division of labor
- Adversarial reasoning or debate

## Anti-Patterns

- **Don't skip `role=`** on member agents — the leader uses roles to decide delegation
- **Don't use teams for simple tasks** — a single agent is faster and cheaper
- **Don't forget `show_members_responses=True`** if you want to see individual contributions
- **Don't mix too many specialists** — 2-4 members is ideal; more creates coordination overhead

## Further Reading

For team modes deep-dive and advanced patterns, read `references/api-patterns.md`.
