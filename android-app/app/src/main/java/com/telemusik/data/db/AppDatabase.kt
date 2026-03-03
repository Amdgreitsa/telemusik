package com.telemusik.data.db

import androidx.room.Database
import androidx.room.RoomDatabase
import com.telemusik.data.model.DownloadedTrack
import com.telemusik.data.model.ListeningHistory
import com.telemusik.data.model.Playlist
import com.telemusik.data.model.PlaylistTrackCrossRef
import com.telemusik.data.model.Track

@Database(
    entities = [Track::class, Playlist::class, PlaylistTrackCrossRef::class, ListeningHistory::class, DownloadedTrack::class],
    version = 1,
)
abstract class AppDatabase : RoomDatabase()
