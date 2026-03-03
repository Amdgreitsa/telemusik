package com.telemusik.data.model

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity
data class Track(
    @PrimaryKey val id: String,
    val title: String,
    val artist: String,
    val durationSec: Int,
    val telegramFileId: Long,
)

@Entity
data class Playlist(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val name: String,
    val smartQuery: String? = null,
)

@Entity(
    primaryKeys = ["playlistId", "trackId"],
    foreignKeys = [
        ForeignKey(entity = Playlist::class, parentColumns = ["id"], childColumns = ["playlistId"], onDelete = ForeignKey.CASCADE),
    ],
    indices = [Index("trackId")]
)
data class PlaylistTrackCrossRef(
    val playlistId: Long,
    val trackId: String,
    val position: Int,
)

@Entity
data class ListeningHistory(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val trackId: String,
    val listenedMs: Long,
    val listenedAt: Long,
)

@Entity
data class DownloadedTrack(
    @PrimaryKey val trackId: String,
    val encryptedPath: String,
    val checksumSha256: String,
    val sizeBytes: Long,
    val downloadedAt: Long,
)
