# Reasoning API Patterns

## ReasoningTools Constructor

```python
from agno.tools.reasoning import ReasoningTools

ReasoningTools(
    add_instructions=True,     # Add reasoning prompts to agent
    think=True,                # Enable think tool
    analyze=True,              # Enable analyze tool
    min_confidence=0.8,        # Minimum confidence threshold
)
```

## Two Approaches to Reasoning

### 1. ReasoningTools (Any Model)

Works with all models by adding reasoning as a tool:

```python
agent = Agent(
    model="openai:gpt-4o",
    tools=[ReasoningTools(add_instructions=True)],
)
```

### 2. Built-in Model Reasoning (Specific Models)

For models with native reasoning (o3, o4-mini, DeepSeek-R1):

```python
agent = Agent(
    model="openai:o3-mini",
    reasoning=True,
)
```

## Streaming Reasoning Content

```python
from agno.run.agent import RunContentEvent

response = agent.run("Complex problem", stream=True)
for event in response:
    if isinstance(event, RunContentEvent):
        print(event.content, end="", flush=True)
```

## Reasoning + Structured Output

```python
from pydantic import BaseModel

class MathSolution(BaseModel):
    steps: list[str]
    answer: float
    confidence: float

agent = Agent(
    model="openai:gpt-4o",
    tools=[ReasoningTools(add_instructions=True)],
    output_schema=MathSolution,
)
```

## Combining with Domain Tools

```python
agent = Agent(
    model="openai:gpt-4o",
    tools=[
        ReasoningTools(add_instructions=True),
        YFinanceTools(),
        CalculatorTools(),
    ],
    instructions=["Think through analysis step by step."],
)
```

## Models with Native Reasoning

| Model | Provider | Notes |
|-------|----------|-------|
| o3-mini | OpenAI | Cost-effective reasoning |
| o3 | OpenAI | Full reasoning |
| o4-mini | OpenAI | Latest reasoning |
| DeepSeek-R1 | DeepSeek | Open-source reasoning |
