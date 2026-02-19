"""
Single Tool Call Reliability Evaluation
=======================================

Demonstrates reliability checks for one expected tool call.
"""

from typing import Optional

from agno.agent import Agent
from agno.eval.reliability import ReliabilityEval, ReliabilityResult
from agno.run.agent import RunOutput
from agno.tools.calculator import CalculatorTools

from cookbook_config import model


# ---------------------------------------------------------------------------
# Create Evaluation Function
# ---------------------------------------------------------------------------
def factorial():
    agent = Agent(
        model=model,
        tools=[CalculatorTools()],
    )
    response: RunOutput = agent.run("What is 10! (ten factorial)?")
    evaluation = ReliabilityEval(
        name="Tool Call Reliability",
        agent_response=response,
        expected_tool_calls=["factorial"],
    )
    result: Optional[ReliabilityResult] = evaluation.run(print_results=True)
    if result:
        result.assert_passed()


# ---------------------------------------------------------------------------
# Run Evaluation
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    factorial()
