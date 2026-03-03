from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        resp = client.get('/health')
        assert resp.status_code == 200
        assert resp.json()['status'] == 'ok'


def test_auth_and_protected_scrobble_queue():
    with TestClient(app) as client:
        auth = client.post('/auth/telegram', json={'telegram_user_id': '100500'})
        assert auth.status_code == 200
        token = auth.json()['access_token']

        denied = client.post('/scrobble/now-playing', json={'artist': 'A', 'track': 'B', 'duration': 180})
        assert denied.status_code == 403

        allowed = client.post(
            '/scrobble/now-playing',
            json={'artist': 'A', 'track': 'B', 'duration': 180},
            headers={'Authorization': f'Bearer {token}'},
        )
        assert allowed.status_code == 200
        assert allowed.json()['queued'] is True
