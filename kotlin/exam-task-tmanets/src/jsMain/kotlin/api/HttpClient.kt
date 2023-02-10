package api

import io.ktor.client.*
import io.ktor.client.engine.js.*
import io.ktor.client.features.json.*
import io.ktor.client.features.json.serializer.*
import io.ktor.client.request.*
import io.ktor.client.request.forms.*
import io.ktor.client.request.parameter
import io.ktor.http.*
import kotlinx.browser.window
import ru.diamant.rabbit.common.model.HistoryResponse
import ru.diamant.rabbit.common.model.StatisticRequest
import ru.diamant.rabbit.common.model.StatisticResponse
import security.UserCredentials

val endpoint = window.location.origin

val httpClient: HttpClient = HttpClient(JsClient()) {
    install(JsonFeature) {
        serializer = KotlinxSerializer()
    }
}

suspend fun getStatistic(request: StatisticRequest): StatisticResponse =
    httpClient.get("$endpoint/api/v1/query") {
        parameter("url", request.url)
        parameter("level", request.level)
    }

suspend fun saveResult(): Unit = httpClient.get("$endpoint/api/v1/save")

suspend fun loadHistory(): HistoryResponse = httpClient.get("$endpoint/api/v1/history")

suspend fun loadHistoryResponse(request: StatisticRequest): StatisticResponse =
    httpClient.get("$endpoint/api/v1/history/get") {
        parameter("url", request.url)
        parameter("level", request.level)
    }

suspend fun deleteHistoryResponse(request: StatisticRequest): Unit =
    httpClient.get("$endpoint/api/v1/history/delete") {
        parameter("url", request.url)
        parameter("level", request.level)

    }

suspend fun loginRequest(credentials: UserCredentials): Boolean =
    httpClient.submitForm(
        url = "$endpoint/api/v1/login",
        formParameters = Parameters.build {
            append("username", credentials.username)
            append("password", credentials.password)
        }
    )

suspend fun logoutRequest(): Unit = httpClient.get("$endpoint/api/v1/logout")