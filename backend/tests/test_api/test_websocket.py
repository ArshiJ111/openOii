from __future__ import annotations


def test_websocket_ping_echo(ws_client):
    with ws_client.websocket_connect("/ws/projects/1") as ws:
        connected = ws.receive_json()
        assert connected["type"] == "connected"
        assert connected["data"]["project_id"] == 1

        ws.send_json({"type": "ping"})
        pong = ws.receive_json()
        assert pong["type"] == "pong"

        ws.send_json({"type": "echo", "data": {"hello": "world"}})
        echo = ws.receive_json()
        assert echo["type"] == "echo"
        assert echo["data"]["hello"] == "world"
