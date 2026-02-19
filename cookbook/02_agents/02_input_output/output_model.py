"""
Output Model
=============================

Use a separate output model to refine the main model's response.

The output_model receives the same conversation but generates its own
response, replacing the main model's output. This is useful when you
want a cheaper model to handle reasoning/tool-use and a more capable
model to produce the final polished answer.

For structured JSON output, use ``parser_model`` instead (see parser_model.py).
"""

from agno.agent import Agent, RunOutput
from rich.pretty import pprint

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=model,
    description="You are a helpful chef that provides detailed recipe information.",
    output_model=model,
    output_model_prompt="You are a world-class culinary writer. Rewrite the recipe with vivid descriptions, pro tips, and elegant formatting.",
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run: RunOutput = agent.run("Give me a recipe for pad thai.")
    pprint(run.content)
