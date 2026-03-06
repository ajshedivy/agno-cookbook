---
name: agno-guardrails
description: |
  Add input and output guardrails to Agno agents. Covers built-in guardrails
  (PII detection, prompt injection), custom guardrails, output validation,
  and moderation. Trigger this skill when: importing agno.guardrails,
  creating guardrail classes, adding pre_hooks or post_hooks, or asking
  "how do I add safety checks to my agent?"
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["guardrails", "safety", "validation", "moderation", "agno"]
---

# Add Guardrails to Agno Agents

Use `pre_hooks` and `post_hooks` to validate inputs and outputs. Install with `pip install agno`.

## Quick Start

```python
from agno.agent import Agent
from agno.guardrails.base import BaseGuardrail
from agno.exceptions import InputCheckError
from agno.run.agent import RunInput

class NoSpamGuardrail(BaseGuardrail):
    def check(self, run_input: RunInput):
        content = run_input.input_content_string()
        if content.count("!") > 10:
            raise InputCheckError("Input appears to be spam")

    async def async_check(self, run_input: RunInput):
        self.check(run_input)

agent = Agent(
    model="openai:gpt-4o",
    pre_hooks=[NoSpamGuardrail()],
)

agent.print_response("Hello!", stream=True)  # OK
agent.print_response("BUY NOW!!!!!!!!!!!!", stream=True)  # Blocked
```

## Input Guardrails (pre_hooks)

Run before the agent processes a message. Raise `InputCheckError` to block:

```python
from agno.guardrails.base import BaseGuardrail
from agno.exceptions import InputCheckError
from agno.run.agent import RunInput

class ContentPolicyGuardrail(BaseGuardrail):
    blocked_topics = ["violence", "illegal"]

    def check(self, run_input: RunInput):
        content = run_input.input_content_string().lower()
        for topic in self.blocked_topics:
            if topic in content:
                raise InputCheckError(f"Blocked topic: {topic}")

    async def async_check(self, run_input: RunInput):
        self.check(run_input)

agent = Agent(
    model="openai:gpt-4o",
    pre_hooks=[ContentPolicyGuardrail()],
)
```

## Output Guardrails (post_hooks)

Run after the agent generates a response. Validate or transform output:

```python
from agno.guardrails.base import BaseOutputGuardrail
from agno.exceptions import OutputCheckError
from agno.run.agent import RunOutput

class NoPIIOutputGuardrail(BaseOutputGuardrail):
    def check(self, run_output: RunOutput):
        import re
        content = str(run_output.output_content_string())
        # Check for email patterns
        if re.search(r'\b[\w.-]+@[\w.-]+\.\w+\b', content):
            raise OutputCheckError("Output contains email addresses")

    async def async_check(self, run_output: RunOutput):
        self.check(run_output)

agent = Agent(
    model="openai:gpt-4o",
    post_hooks=[NoPIIOutputGuardrail()],
)
```

## Built-in Guardrails

### PII Detection

```python
from agno.guardrails import PIIDetectionGuardrail

agent = Agent(
    model="openai:gpt-4o",
    pre_hooks=[PIIDetectionGuardrail()],
)
```

### Prompt Injection Detection

```python
from agno.guardrails import PromptInjectionGuardrail

agent = Agent(
    model="openai:gpt-4o",
    pre_hooks=[PromptInjectionGuardrail()],
)
```

### Combining Multiple Guardrails

```python
agent = Agent(
    model="openai:gpt-4o",
    pre_hooks=[
        PIIDetectionGuardrail(),
        PromptInjectionGuardrail(),
        ContentPolicyGuardrail(),
    ],
    post_hooks=[
        NoPIIOutputGuardrail(),
    ],
)
```

## Custom Guardrail with Model-Based Checking

Use an LLM to classify inputs:

```python
from agno.agent import Agent
from agno.guardrails.base import BaseGuardrail
from agno.exceptions import InputCheckError
from agno.run.agent import RunInput

class ToxicityGuardrail(BaseGuardrail):
    def __init__(self):
        self.classifier = Agent(
            model="openai:gpt-4o-mini",
            instructions=[
                "Classify the input as 'safe' or 'toxic'.",
                "Respond with only one word: safe or toxic.",
            ],
        )

    def check(self, run_input: RunInput):
        content = run_input.input_content_string()
        result = self.classifier.run(content)
        if "toxic" in str(result.content).lower():
            raise InputCheckError("Input classified as toxic")

    async def async_check(self, run_input: RunInput):
        content = run_input.input_content_string()
        result = await self.classifier.arun(content)
        if "toxic" in str(result.content).lower():
            raise InputCheckError("Input classified as toxic")
```

## Handling Guardrail Errors

```python
from agno.exceptions import InputCheckError, OutputCheckError

try:
    response = agent.run("Some potentially bad input")
except InputCheckError as e:
    print(f"Input blocked: {e}")
except OutputCheckError as e:
    print(f"Output blocked: {e}")
```

## Anti-Patterns

- **Don't forget `async_check`** — both sync and async methods must be implemented
- **Don't use expensive guardrails for every message** — balance safety with latency
- **Don't silently swallow errors** — raise `InputCheckError` or `OutputCheckError` to block
- **Don't put business logic in guardrails** — they're for safety and validation only
- **Don't rely solely on guardrails** — they complement, not replace, proper prompt engineering

## Further Reading

For OpenAI moderation integration and advanced patterns, read `references/api-patterns.md`.
