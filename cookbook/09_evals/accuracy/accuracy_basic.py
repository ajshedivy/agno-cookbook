"""
Basic Accuracy Evaluation
=========================

Demonstrates synchronous and asynchronous accuracy evaluations.
"""

import asyncio
from typing import Optional

from agno.agent import Agent
from agno.eval.accuracy import AccuracyEval, AccuracyResult
from agno.tools.calculator import CalculatorTools

from cookbook_config import model

# ---------------------------------------------------------------------------
# Create Sync Evaluation
# ---------------------------------------------------------------------------
evaluation = AccuracyEval(
    name="Calculator Evaluation",
    model=model,
    agent=Agent(
        model=model,
        tools=[CalculatorTools()],
    ),
    input="What is 10*5 then to the power of 2? do it step by step",
    expected_output="2500",
    additional_guidelines="Agent output should include the steps and the final answer.",
    num_iterations=1,
)

# ---------------------------------------------------------------------------
# Create Async Evaluation
# ---------------------------------------------------------------------------
async_evaluation = AccuracyEval(
    model=model,
    agent=Agent(
        model=model,
        tools=[CalculatorTools()],
    ),
    input="What is 10*5 then to the power of 2? do it step by step",
    expected_output="2500",
    additional_guidelines="Agent output should include the steps and the final answer.",
    num_iterations=3,
)

# ---------------------------------------------------------------------------
# Run Evaluation
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    result: Optional[AccuracyResult] = evaluation.run(print_results=True)
    assert result is not None and result.avg_score >= 8

    async_result: Optional[AccuracyResult] = asyncio.run(async_evaluation.arun(print_results=True))
    assert async_result is not None and async_result.avg_score >= 8
