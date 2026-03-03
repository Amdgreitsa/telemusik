package com.telemusik.data.db.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.telemusik.data.model.Playlist
import kotlinx.coroutines.flow.Flow

@Dao
interface PlaylistDao {
    @Query("SELECT * FROM Playlist ORDER BY id DESC")
    fun observePlaylists(): Flow<List<Playlist>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(playlist: Playlist): Long

    @Query("DELETE FROM Playlist WHERE id = :playlistId")
    suspend fun deleteById(playlistId: Long)
}
