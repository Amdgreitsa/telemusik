from pydantic import BaseModel


class ApkInfo(BaseModel):
    version: str
    download_url: str


class ChangelogItem(BaseModel):
    version: str
    changelog: str


class AuthRequest(BaseModel):
    telegram_user_id: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class ScrobbleNowPlaying(BaseModel):
    artist: str
    track: str
    duration: int


class ScrobbleSubmit(ScrobbleNowPlaying):
    played_at: int


class QueueProcessResponse(BaseModel):
    processed: int
    failed: int
