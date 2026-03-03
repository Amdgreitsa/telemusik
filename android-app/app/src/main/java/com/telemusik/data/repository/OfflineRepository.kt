package com.telemusik.data.repository

import com.telemusik.data.db.dao.DownloadedTrackDao
import com.telemusik.data.model.DownloadedTrack
import kotlinx.coroutines.flow.Flow
import java.io.File
import java.security.MessageDigest

class OfflineRepository(
    private val downloadedTrackDao: DownloadedTrackDao,
) {
    fun observeDownloads(): Flow<List<DownloadedTrack>> = downloadedTrackDao.observeDownloads()

    suspend fun saveDownloadedTrack(item: DownloadedTrack) {
        downloadedTrackDao.upsert(item)
    }

    fun verifyChecksum(path: String, expectedSha256: String): Boolean {
        val file = File(path)
        if (!file.exists() || !file.isFile) return false
        val digest = MessageDigest.getInstance("SHA-256")
        file.inputStream().use { input ->
            val buf = ByteArray(8192)
            while (true) {
                val read = input.read(buf)
                if (read <= 0) break
                digest.update(buf, 0, read)
            }
        }
        val hash = digest.digest().joinToString("") { b -> "%02x".format(b) }
        return hash.equals(expectedSha256, ignoreCase = true)
    }

    suspend fun enforceCacheLimit(maxBytes: Long) {
        if (maxBytes <= 0) return
        var total = downloadedTrackDao.getTotalSizeBytes()
        if (total <= maxBytes) return

        val oldest = downloadedTrackDao.getOldestFirst()
        for (track in oldest) {
            File(track.encryptedPath).delete()
            downloadedTrackDao.delete(track.trackId)
            total -= track.sizeBytes
            if (total <= maxBytes) break
        }
    }
}
