from __future__ import annotations

import pytest

from app.config import Settings
from app.services.image import ImageService


def test_build_url():
    settings = Settings(
        database_url="sqlite+aiosqlite:///:memory:",
        image_base_url="https://img.example.com/",
        image_endpoint="images/generations",
    )
    service = ImageService(settings)
    assert service._build_url() == "https://img.example.com/images/generations"


@pytest.mark.asyncio
async def test_generate_url_dalle(monkeypatch):
    settings = Settings(
        database_url="sqlite+aiosqlite:///:memory:",
        image_base_url="https://img.example.com",
        image_endpoint="/images/generations",
        image_api_key="test",
    )
    service = ImageService(settings)

    async def fake_post(url, payload):
        return {"data": [{"url": "https://cdn.example.com/image.png"}]}

    monkeypatch.setattr(service, "_post_json_with_retry", fake_post)

    url = await service.generate_url(prompt="cat")
    assert url == "https://cdn.example.com/image.png"


@pytest.mark.asyncio
async def test_generate_url_chat_completions(monkeypatch):
    settings = Settings(
        database_url="sqlite+aiosqlite:///:memory:",
        image_base_url="https://img.example.com",
        image_endpoint="/chat/completions",
        image_api_key="test",
    )
    service = ImageService(settings)

    async def fake_stream(url, payload):
        return "result https://cdn.example.com/stream.png done"

    monkeypatch.setattr(service, "_post_stream_with_retry", fake_stream)

    url = await service.generate_url(prompt="cat")
    assert url == "https://cdn.example.com/stream.png"


@pytest.mark.asyncio
async def test_generate_url_modelscope(monkeypatch):
    settings = Settings(
        database_url="sqlite+aiosqlite:///:memory:",
        image_base_url="https://api.modelscope.cn",
        image_endpoint="/v1/images/generations",
        image_api_key="test",
    )
    service = ImageService(settings)

    async def fake_modelscope(prompt):
        return "https://modelscope.example.com/image.png"

    monkeypatch.setattr(service, "_modelscope_generate", fake_modelscope)

    url = await service.generate_url(prompt="cat")
    assert url == "https://modelscope.example.com/image.png"


@pytest.mark.asyncio
async def test_generate_url_fallback_from_i2i(monkeypatch):
    settings = Settings(
        database_url="sqlite+aiosqlite:///:memory:",
        image_base_url="https://img.example.com",
        image_endpoint="/images/generations",
        image_api_key="test",
        enable_image_to_image=True,
    )
    service = ImageService(settings)

    async def fail_post(url, payload):
        raise RuntimeError("boom")

    async def fake_generate(*args, **kwargs):
        return {"data": [{"url": "https://cdn.example.com/fallback.png"}]}

    monkeypatch.setattr(service, "_post_json_with_retry", fail_post)
    monkeypatch.setattr(service, "generate", fake_generate)

    url = await service.generate_url(prompt="cat", image_bytes=b"fake")
    assert url == "https://cdn.example.com/fallback.png"
