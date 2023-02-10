package ru.diamant.rabbit.application

import io.ktor.server.engine.*
import io.ktor.server.netty.*
import ru.diamant.rabbit.application.plugins.configureRouting
import ru.diamant.rabbit.application.plugins.configureSecurity
import ru.diamant.rabbit.application.plugins.configureSerialization


fun main() {
    embeddedServer(Netty, port = 8080, host = "127.0.0.1") {
        configureSecurity()
        configureRouting()
        configureSerialization()
    }.start(wait = true)

}