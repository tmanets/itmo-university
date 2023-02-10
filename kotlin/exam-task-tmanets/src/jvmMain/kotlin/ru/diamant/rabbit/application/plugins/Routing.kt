package ru.diamant.rabbit.application.plugins

import io.ktor.application.*
import io.ktor.html.*
import io.ktor.http.*
import io.ktor.http.content.*
import io.ktor.request.*
import io.ktor.routing.*
import io.ktor.response.*
import io.ktor.sessions.*
import kotlinx.html.*
import ru.diamant.rabbit.application.templates.index
import ru.diamant.rabbit.application.workers.History
import ru.diamant.rabbit.application.workers.processStatistic
import ru.diamant.rabbit.common.model.StatisticRequest
import ru.diamant.rabbit.common.model.StatisticResponse
import ru.diamant.rabbit.common.model.UserSession

const val AUTHENTICATION_SUCCESS = true
const val AUTHENTICATION_FAIL = false

fun Application.configureRouting() {
    routing {
        configureApi()

        // must be last
        configureWeb()
    }
}

fun Routing.configureWeb() {

    get("*") {
        call.respondHtml(HttpStatusCode.OK, HTML::index)
    }
    //добавил чтобы можно было зайти в браузере по ссылке 127.0.0.1:8080/ (до этого не открывалось)
    get("/") {
        call.respondHtml(HttpStatusCode.OK, HTML::index)
    }

    static("/static") {
        resources()
    }
}

fun Routing.configureApi() {
    route("/api/v1") {
        configurePublicApi()
        configureAuthorizedApi()
    }

}

fun Route.configurePublicApi() {
    get("/query") {
        val url = call.request.queryParameters["url"] ?: error("Error parsing parameter 'url'")
        val level = call.request.queryParameters["level"]?.toInt() ?: error("Error parsing parameter 'level'")

        val response = processStatistic(StatisticRequest(url, level))

        if (Session.isAuthorised()) {
            Session.set(StatisticRequest(url, level), response)
            println("session ${Session.get()}")
        }
        println(response)
        call.respond(HttpStatusCode.OK, response)
    }

    post("/login") {
        val params = call.receiveParameters()
        val username = params["username"] ?: error("Error parsing parameter 'username'")
        val password = params["password"] ?: error("Error parsing parameter 'password'")

        val user = validate(username, password)
        println("logged in user: $user")

        if (user == null) {
            call.respond(HttpStatusCode.OK, AUTHENTICATION_FAIL)
        } else {
            Session.setDefault(username)
            call.respond(HttpStatusCode.OK, AUTHENTICATION_SUCCESS)
        }
    }
}

fun Route.configureAuthorizedApi() {
    get("/save") {
        println("saving")
        println(Session.get())
        if (Session.isAuthorised()) { //кажется здесь я гарантирую, что userSession != null
            val userSession = Session.get()
            History.save(
                userSession!!.username,
                userSession.lastRequest,
                userSession.lastResponse,
            )
            println(History.getRequests(userSession.username))
        }
        call.respond(HttpStatusCode.OK)
    }
    get("/history") {
        val userSession = Session.get() ?: error("Not authorized")
        val data = History.getRequests(userSession.username)
        println(data)
        call.respond(HttpStatusCode.OK, data)
    }

    get("/history/get") {
        val url = call.request.queryParameters["url"] ?: error("Error parsing parameter 'url'")
        val level = call.request.queryParameters["level"]?.toInt() ?: error("Error parsing parameter 'level'")
        val userSession = Session.get() ?: error("Not authorized")
        val data = History.getResponse(userSession.username, StatisticRequest(url, level))
        println(data)
        call.respond(HttpStatusCode.OK, data)
    }

    get("/history/delete") {
        val url = call.request.queryParameters["url"] ?: error("Error parsing parameter 'url'")
        val level = call.request.queryParameters["level"]?.toInt() ?: error("Error parsing parameter 'level'")
        val userSession = Session.get() ?: error("Not authorized")
        History.deleteResponse(userSession.username, StatisticRequest(url, level))
        call.respond(HttpStatusCode.OK)
    }

    get("/logout") {
        Session.clear()
        println("logged out")
        call.respond(HttpStatusCode.OK)
    }
}