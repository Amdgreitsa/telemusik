package com.telemusik.data.db.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.telemusik.data.model.DownloadedTrack
import kotlinx.coroutines.flow.Flow

@Dao
interface DownloadedTrackDao {
    @Query("SELECT * FROM DownloadedTrack ORDER BY downloadedAt DESC")
    fun observeDownloads(): Flow<List<DownloadedTrack>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(item: DownloadedTrack)

    @Query("DELETE FROM DownloadedTrack WHERE trackId = :trackId")
    suspend fun delete(trackId: String)
}
