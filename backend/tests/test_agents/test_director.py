from __future__ import annotations

import json

import pytest
from sqlmodel import select

from app.agents.director import DirectorAgent
from app.models.message import Message
from tests.agent_fixtures import FakeLLM, make_context


@pytest.mark.asyncio
async def test_director_updates_project_and_sends_messages(test_session, test_settings):
    payload = {
        "project_update": {"style": "noir", "status": "planning"},
        "director_notes": {"vision": "Dark tone"},
        "scene_outline": [{"title": "Scene 1"}],
    }
    llm = FakeLLM(json.dumps(payload))
    ctx = await make_context(test_session, test_settings, llm=llm)

    agent = DirectorAgent()
    await agent.run(ctx)

    await test_session.refresh(ctx.project)
    assert ctx.project.style == "noir"

    res = await test_session.execute(select(Message).where(Message.run_id == ctx.run.id))
    assert len(res.scalars().all()) >= 2
