package ru.diamant.rabbit.common.model

import kotlinx.serialization.Serializable

@Serializable
data class HistoryResponse(
    val response: List<StatisticRequest>
)
