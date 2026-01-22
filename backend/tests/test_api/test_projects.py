from __future__ import annotations

import pytest

from tests.factories import create_project


@pytest.mark.asyncio
async def test_list_projects_empty(async_client):
    res = await async_client.get("/api/v1/projects")
    assert res.status_code == 200
    data = res.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_list_projects_with_data(async_client, test_session):
    await create_project(test_session, title="Project 1")
    await create_project(test_session, title="Project 2")

    res = await async_client.get("/api/v1/projects")
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) == 2
    assert data["total"] == 2


@pytest.mark.asyncio
async def test_create_project(async_client):
    res = await async_client.post(
        "/api/v1/projects",
        json={"title": "New Project", "description": "Test", "story": "Once upon a time"},
    )
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "New Project"
    assert data["status"] == "draft"


@pytest.mark.asyncio
async def test_get_project(async_client, test_session):
    project = await create_project(test_session, title="Get Test")
    res = await async_client.get(f"/api/v1/projects/{project.id}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == project.id
    assert data["title"] == "Get Test"


@pytest.mark.asyncio
async def test_get_project_not_found(async_client):
    res = await async_client.get("/api/v1/projects/99999")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_update_project(async_client, test_session):
    project = await create_project(test_session, title="Old Title")
    res = await async_client.patch(
        f"/api/v1/projects/{project.id}",
        json={"title": "New Title", "style": "noir"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == "New Title"
    assert data["style"] == "noir"


@pytest.mark.asyncio
async def test_delete_project(async_client, test_session):
    project = await create_project(test_session)
    res = await async_client.delete(f"/api/v1/projects/{project.id}")
    assert res.status_code == 204

    res = await async_client.get(f"/api/v1/projects/{project.id}")
    assert res.status_code == 404
