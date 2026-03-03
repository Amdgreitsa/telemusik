package com.telemusik.data.repository

import com.telemusik.data.db.dao.DownloadedTrackDao
import com.telemusik.data.model.DownloadedTrack
import kotlinx.coroutines.flow.Flow

class OfflineRepository(
    private val downloadedTrackDao: DownloadedTrackDao,
) {
    fun observeDownloads(): Flow<List<DownloadedTrack>> = downloadedTrackDao.observeDownloads()
}
