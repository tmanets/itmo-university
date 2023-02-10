package ru.diamant.rabbit.common.model

import kotlinx.serialization.Serializable

@Serializable
data class UserSession(
    val username: String,
    var lastRequest: StatisticRequest?,
    var lastResponse: StatisticResponse?
)
