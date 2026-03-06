---
name: agno-reasoning
description: |
  Add reasoning and chain-of-thought capabilities to Agno agents. Covers
  ReasoningTools, built-in model reasoning, reasoning content streaming,
  and structured problem solving. Trigger this skill when: importing
  agno.tools.reasoning, enabling chain-of-thought, building agents that
  think step-by-step, or asking "how do I add reasoning to my agent?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["reasoning", "chain-of-thought", "thinking", "agno"]
---

# Add Reasoning to Agno Agents

Use `ReasoningTools` or built-in model reasoning to give agents step-by-step thinking. Install with `pip install agno`.

## Quick Start — ReasoningTools

The simplest way to add reasoning. Works with any model:

```python
from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools

agent = Agent(
    model="openai:gpt-4o",
    tools=[ReasoningTools(add_instructions=True)],
    markdown=True,
)

agent.print_response(
    "How many r's are in the word 'strawberry'?",
    stream=True,
)
```

## ReasoningTools Configuration

```python
from agno.tools.reasoning import ReasoningTools

ReasoningTools(
    add_instructions=True,     # Add reasoning instructions to agent
    think=True,                # Enable thinking tool
    analyze=True,              # Enable analysis tool
    min_confidence=0.8,        # Minimum confidence threshold
)
```

## Built-in Model Reasoning

Some models have native reasoning capabilities. Enable with `reasoning=True`:

```python
from agno.agent import Agent

agent = Agent(
    model="openai:o3-mini",
    reasoning=True,
    markdown=True,
)

agent.print_response("Solve: If a train leaves at 3pm...", stream=True)
```

## Streaming Reasoning Content

Capture and display the agent's reasoning process:

```python
from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools
from agno.run.agent import RunContentEvent

agent = Agent(
    model="openai:gpt-4o",
    tools=[ReasoningTools(add_instructions=True)],
)

response = agent.run("What is 27 * 43?", stream=True)

for event in response:
    if isinstance(event, RunContentEvent):
        print(event.content, end="", flush=True)
```

## Reasoning for Complex Problems

ReasoningTools shines on logic puzzles, math, and multi-step problems:

```python
from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools

agent = Agent(
    model="openai:gpt-4o",
    tools=[ReasoningTools(add_instructions=True)],
    instructions=[
        "Break problems into clear steps.",
        "Show your reasoning before giving the answer.",
    ],
    markdown=True,
)

agent.print_response(
    "A farmer has 17 sheep. All but 9 die. How many are left?",
    stream=True,
)
```

## Reasoning with Other Tools

Combine reasoning with domain tools for analytical tasks:

```python
from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

agent = Agent(
    model="openai:gpt-4o",
    tools=[
        ReasoningTools(add_instructions=True),
        YFinanceTools(),
    ],
    instructions=[
        "Think through investment analysis step by step.",
        "Consider both bull and bear cases.",
    ],
    markdown=True,
)

agent.print_response("Should I invest in NVIDIA right now?", stream=True)
```

## Reasoning in Teams

Add reasoning to individual team members for deeper analysis:

```python
from agno.agent import Agent
from agno.team.team import Team
from agno.tools.reasoning import ReasoningTools

analyst = Agent(
    name="Analyst",
    role="Deep analytical thinker",
    model="openai:gpt-4o",
    tools=[ReasoningTools(add_instructions=True)],
    instructions=["Think step-by-step through analysis."],
)

writer = Agent(
    name="Writer",
    role="Clear communicator",
    model="openai:gpt-4o",
    instructions=["Summarize analysis into clear prose."],
)

team = Team(
    name="Analysis Team",
    model="openai:gpt-4o",
    members=[analyst, writer],
    show_members_responses=True,
    markdown=True,
)
```

## Anti-Patterns

- **Don't add reasoning to simple Q&A agents** — it adds latency without value
- **Don't use both `ReasoningTools` and `reasoning=True`** — pick one approach
- **Don't skip `add_instructions=True`** on ReasoningTools — the agent needs guidance
- **Don't expect reasoning to fix bad prompts** — reasoning amplifies good instructions
- **Don't use reasoning-native models (o3) with ReasoningTools** — they already reason internally

## Further Reading

For model-specific reasoning options and advanced patterns, read `references/api-patterns.md`.
