from __future__ import annotations

import pytest
from sqlmodel import select

from app.agents.character_artist import CharacterArtistAgent
from app.models.project import Character
from tests.agent_fixtures import FakeImageService, FakeLLM, make_context
from tests.factories import create_character, create_project, create_run


@pytest.mark.asyncio
async def test_character_artist_generates_images(test_session, test_settings):
    project = await create_project(test_session)
    run = await create_run(test_session, project_id=project.id)
    character = await create_character(test_session, project_id=project.id, image_url=None)

    image = FakeImageService(url="http://image.test/hero.png")
    ctx = await make_context(
        test_session,
        test_settings,
        project=project,
        run=run,
        llm=FakeLLM("{}"),
        image=image,
    )

    agent = CharacterArtistAgent()
    await agent.run(ctx)

    await test_session.refresh(character)
    assert character.image_url == "http://image.test/hero.png"
    assert any(event[1]["type"] == "character_updated" for event in ctx.ws.events)

    res = await test_session.execute(select(Character).where(Character.project_id == project.id))
    assert len(res.scalars().all()) == 1
