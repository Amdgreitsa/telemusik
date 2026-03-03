package com.telemusik.domain.scrobble

class LastFmScrobbler {
    fun shouldScrobble(positionSec: Long, durationSec: Long): Boolean {
        if (durationSec <= 0) return false
        return positionSec >= 240 || positionSec >= durationSec / 2
    }
}
