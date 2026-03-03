from pydantic import BaseModel


class ApkInfo(BaseModel):
    version: str
    download_url: str


class ChangelogItem(BaseModel):
    version: str
    changelog: str


class ScrobbleNowPlaying(BaseModel):
    user_id: int
    artist: str
    track: str
    duration: int


class ScrobbleSubmit(ScrobbleNowPlaying):
    played_at: int
