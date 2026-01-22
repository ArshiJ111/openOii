from __future__ import annotations

import json

import pytest
from sqlmodel import select

from app.agents.scriptwriter import ScriptwriterAgent
from app.models.project import Character, Scene, Shot
from tests.agent_fixtures import FakeLLM, make_context


@pytest.mark.asyncio
async def test_scriptwriter_creates_characters_scenes_and_shots(test_session, test_settings):
    payload = {
        "project_update": {"status": "scripted"},
        "characters": [{"name": "Hero", "description": "Brave"}],
        "scenes": [
            {
                "order": 1,
                "description": "Scene 1",
                "shot_plan": [{"description": "Shot 1", "prompt": "Action"}],
            }
        ],
    }
    llm = FakeLLM(json.dumps(payload))
    ctx = await make_context(test_session, test_settings, llm=llm)

    agent = ScriptwriterAgent()
    await agent.run(ctx)

    res = await test_session.execute(select(Character).where(Character.project_id == ctx.project.id))
    assert len(res.scalars().all()) == 1

    res = await test_session.execute(select(Scene).where(Scene.project_id == ctx.project.id))
    assert len(res.scalars().all()) == 1

    res = await test_session.execute(
        select(Shot).join(Scene).where(Scene.project_id == ctx.project.id)
    )
    assert len(res.scalars().all()) == 1
