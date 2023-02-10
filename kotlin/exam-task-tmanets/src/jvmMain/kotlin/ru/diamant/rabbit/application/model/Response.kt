package ru.diamant.rabbit.application.model

import ru.diamant.rabbit.common.model.StatisticRequest

//Здесь храним все запросы
data class Response(
    val user: String,
    val request: StatisticRequest,
    val words: List<String>,
    val images: List<Int>
) {
    val id = "$user${request.level}${request.url}".hashCode()
}
