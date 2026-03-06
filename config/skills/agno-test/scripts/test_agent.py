"""
Test Agent Template
====================
Template pytest script for testing agents via AgentOSClient.

Prerequisites:
    1. Start an AgentOS server: python start_agentos.py
    2. Install test dependencies: pip install pytest pytest-asyncio
    3. Run tests: pytest test_agent.py -v

Usage:
    pytest test_agent.py -v
"""

import asyncio

import pytest
from agno.client import AgentOSClient
from agno.run.agent import RunCompletedEvent, RunContentEvent

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_URL = "http://localhost:7777"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def client():
    """Create an AgentOSClient instance."""
    return AgentOSClient(base_url=BASE_URL)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_server_is_running(client):
    """Verify the AgentOS server is running and reachable."""
    config = await client.aget_config()
    assert config is not None
    assert len(config.agents or []) > 0, "No agents registered"


@pytest.mark.asyncio
async def test_agent_non_streaming(client):
    """Test running an agent without streaming."""
    config = await client.aget_config()
    agent_id = config.agents[0].id

    result = await client.run_agent(
        agent_id=agent_id,
        message="What is 2 + 2? Reply with just the number.",
    )

    assert result.content is not None
    assert result.run_id is not None
    assert "4" in str(result.content)


@pytest.mark.asyncio
async def test_agent_streaming(client):
    """Test running an agent with streaming."""
    config = await client.aget_config()
    agent_id = config.agents[0].id

    chunks = []
    completed = False

    async for event in client.run_agent_stream(
        agent_id=agent_id,
        message="Say 'hello world' and nothing else.",
    ):
        if isinstance(event, RunContentEvent):
            chunks.append(event.content)
        elif isinstance(event, RunCompletedEvent):
            completed = True

    full_response = "".join(chunks)
    assert len(full_response) > 0, "No content received"
    assert "hello" in full_response.lower()


@pytest.mark.asyncio
async def test_session_persistence(client):
    """Test that conversations persist within a session."""
    config = await client.aget_config()
    agent_id = config.agents[0].id
    session_id = "test-session-persistence"

    # First message
    await client.run_agent(
        agent_id=agent_id,
        message="Remember this number: 42",
        session_id=session_id,
    )

    # Second message — should remember
    result = await client.run_agent(
        agent_id=agent_id,
        message="What number did I ask you to remember?",
        session_id=session_id,
    )

    assert "42" in str(result.content)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
