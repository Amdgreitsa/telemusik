package com.telemusik.domain.recommendations

import com.telemusik.data.model.ListeningHistory

class RecommendationEngine {
    fun score(history: List<ListeningHistory>): List<String> {
        return history.groupBy { it.trackId }
            .mapValues { entry -> entry.value.sumOf { it.listenedMs } }
            .toList()
            .sortedByDescending { it.second }
            .map { it.first }
    }
}
