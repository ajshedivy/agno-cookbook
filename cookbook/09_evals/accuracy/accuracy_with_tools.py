"""
Tool-Enabled Accuracy Evaluation
================================

Demonstrates accuracy evaluation for an agent using calculator tools.
"""

from typing import Optional

from agno.agent import Agent
from agno.eval.accuracy import AccuracyEval, AccuracyResult
from agno.tools.calculator import CalculatorTools

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Evaluation
# ---------------------------------------------------------------------------
evaluation = AccuracyEval(
    name="Tools Evaluation",
    model=model,
    agent=Agent(
        model=model,
        tools=[CalculatorTools()],
    ),
    input="What is 10!?",
    expected_output="3628800",
)

# ---------------------------------------------------------------------------
# Run Evaluation
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    result: Optional[AccuracyResult] = evaluation.run(print_results=True)
    assert result is not None and result.avg_score >= 8
