import hashlib
from urllib.parse import urlencode

import httpx

from app.core.config import settings


LASTFM_BASE = 'https://ws.audioscrobbler.com/2.0/'


def _sign(params: dict[str, str]) -> str:
    payload = ''.join(f'{k}{params[k]}' for k in sorted(params)) + settings.lastfm_api_secret
    return hashlib.md5(payload.encode()).hexdigest()


async def now_playing(session_key: str, artist: str, track: str, duration: int) -> dict:
    data = {
        'method': 'track.updateNowPlaying',
        'api_key': settings.lastfm_api_key,
        'artist': artist,
        'track': track,
        'duration': str(duration),
        'sk': session_key,
        'format': 'json',
    }
    data['api_sig'] = _sign(data)
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(LASTFM_BASE, data=urlencode(data), headers={'Content-Type': 'application/x-www-form-urlencoded'})
        resp.raise_for_status()
        return resp.json()


async def scrobble(session_key: str, artist: str, track: str, played_at: int) -> dict:
    data = {
        'method': 'track.scrobble',
        'api_key': settings.lastfm_api_key,
        'artist': artist,
        'track': track,
        'timestamp': str(played_at),
        'sk': session_key,
        'format': 'json',
    }
    data['api_sig'] = _sign(data)
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(LASTFM_BASE, data=urlencode(data), headers={'Content-Type': 'application/x-www-form-urlencoded'})
        resp.raise_for_status()
        return resp.json()
