from __future__ import annotations

import pytest

from tests.factories import create_project, create_scene


@pytest.mark.asyncio
async def test_list_scenes(async_client, test_session):
    project = await create_project(test_session)
    await create_scene(test_session, project_id=project.id, order=1)
    await create_scene(test_session, project_id=project.id, order=2)

    res = await async_client.get(f"/api/v1/projects/{project.id}/scenes")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 2
    assert data[0]["order"] == 1


@pytest.mark.asyncio
async def test_update_scene(async_client, test_session):
    project = await create_project(test_session)
    scene = await create_scene(test_session, project_id=project.id, description="Old")

    res = await async_client.patch(
        f"/api/v1/scenes/{scene.id}",
        json={"description": "New description"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["description"] == "New description"


@pytest.mark.asyncio
async def test_update_scene_not_found(async_client):
    res = await async_client.patch(
        "/api/v1/scenes/99999",
        json={"description": "Test"},
    )
    assert res.status_code == 404
