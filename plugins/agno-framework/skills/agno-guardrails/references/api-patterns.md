# Guardrails API Patterns

## Input Guardrail Base Class

```python
from agno.guardrails.base import BaseGuardrail
from agno.exceptions import InputCheckError
from agno.run.agent import RunInput

class MyGuardrail(BaseGuardrail):
    def check(self, run_input: RunInput):
        content = run_input.input_content_string()
        if not_valid(content):
            raise InputCheckError("Validation failed")

    async def async_check(self, run_input: RunInput):
        self.check(run_input)
```

## Output Guardrail Base Class

```python
from agno.guardrails.base import BaseOutputGuardrail
from agno.exceptions import OutputCheckError
from agno.run.agent import RunOutput

class MyOutputGuardrail(BaseOutputGuardrail):
    def check(self, run_output: RunOutput):
        content = str(run_output.output_content_string())
        if not_valid(content):
            raise OutputCheckError("Output validation failed")

    async def async_check(self, run_output: RunOutput):
        self.check(run_output)
```

## Built-in Guardrails

| Guardrail | Import | Purpose |
|-----------|--------|---------|
| PII Detection | `agno.guardrails.PIIDetectionGuardrail` | Block PII in input |
| Prompt Injection | `agno.guardrails.PromptInjectionGuardrail` | Block injection attempts |

## RunInput Properties

```python
run_input.input_content_string()   # Get input as plain text
run_input.messages                  # Raw message list
```

## RunOutput Properties

```python
run_output.output_content_string()  # Get output as plain text
run_output.content                   # Raw content object
```

## Error Handling

```python
from agno.exceptions import InputCheckError, OutputCheckError

try:
    response = agent.run("user input")
except InputCheckError as e:
    print(f"Input blocked: {e}")
except OutputCheckError as e:
    print(f"Output blocked: {e}")
```

## Guardrail with Configuration

```python
class RateLimitGuardrail(BaseGuardrail):
    """Guardrails can use Pydantic fields for configuration."""
    max_requests_per_minute: int = 60
    request_counts: dict = {}

    def check(self, run_input: RunInput):
        # Rate limiting logic
        ...

    async def async_check(self, run_input: RunInput):
        self.check(run_input)
```

## Combining Pre and Post Hooks

```python
agent = Agent(
    model="openai:gpt-4o",
    pre_hooks=[                          # Input validation
        PIIDetectionGuardrail(),
        PromptInjectionGuardrail(),
        LengthGuardrail(max_length=5000),
    ],
    post_hooks=[                         # Output validation
        NoPIIOutputGuardrail(),
        FormatCheckGuardrail(),
    ],
)
```
