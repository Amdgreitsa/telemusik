from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        resp = client.get('/health')
        assert resp.status_code == 200
        assert resp.json()['status'] == 'ok'
        assert resp.headers.get('x-request-id')


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


def test_deduplicates_scrobble_submit():
    with TestClient(app) as client:
        auth = client.post('/auth/telegram', json={'telegram_user_id': '200'})
        token = auth.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        payload = {'artist': 'Artist', 'track': 'Track', 'duration': 210, 'played_at': 1710000000}

        first = client.post('/scrobble/submit', json=payload, headers=headers)
        second = client.post('/scrobble/submit', json=payload, headers=headers)

        assert first.status_code == 200
        assert second.status_code == 200
        assert first.json()['queue_id'] == second.json()['queue_id']


def test_scrobble_process_requires_admin_key():
    with TestClient(app) as client:
        response = client.post('/scrobble/process?session_key=abc')
        assert response.status_code == 403
