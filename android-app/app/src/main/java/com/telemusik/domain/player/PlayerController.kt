package com.telemusik.domain.player

import android.content.Context
import androidx.media3.common.MediaItem
import androidx.media3.common.Player
import androidx.media3.exoplayer.ExoPlayer

class PlayerController(context: Context) {
    private val player: ExoPlayer = ExoPlayer.Builder(context).build()

    fun setQueue(urls: List<String>) {
        player.setMediaItems(urls.map { MediaItem.fromUri(it) })
        player.prepare()
    }

    fun play(index: Int = 0) {
        player.seekTo(index, 0)
        player.playWhenReady = true
    }

    fun setShuffle(enabled: Boolean) {
        player.shuffleModeEnabled = enabled
    }

    fun setRepeat(mode: Int) {
        player.repeatMode = mode
    }

    fun release() = player.release()

    fun addCompletionListener(onFinished: () -> Unit) {
        player.addListener(object : Player.Listener {
            override fun onPlaybackStateChanged(playbackState: Int) {
                if (playbackState == Player.STATE_ENDED) onFinished()
            }
        })
    }
}
