package ru.diamant.rabbit.application.plugins

import io.ktor.application.*
import io.ktor.auth.*
import io.ktor.sessions.*
import io.ktor.util.*
import ru.diamant.rabbit.common.model.StatisticRequest
import ru.diamant.rabbit.common.model.StatisticResponse
import ru.diamant.rabbit.common.model.UserSession

val EMPTY_SESSION = null

/*
по хорошему конечно не надо хранить таблицу здесь
но пока и регистрации нет))
*/
val digestFunction = getDigestFunction("SHA-256") { "ktor${it.length}" }

val hashedUserTable = UserHashedTableAuth(
    table = mapOf(
        "test" to digestFunction("test"),
        "admin" to digestFunction("password")
    ),
    digester = digestFunction
)

/*
предполагалось использовать плагин, но у меня он нормально не работал
а вернее я скорее всего его не правильно использовал
сессия у меня произвольно обнулялась
поэтому было решено использовать самописный класс
*/
class Session {
    companion object {
        private var userSession: UserSession? = EMPTY_SESSION

        fun get(): UserSession? = userSession
        fun isAuthorised(): Boolean = (userSession != EMPTY_SESSION)
        fun setDefault(username: String) {
            userSession = UserSession(username, null, null)
        }

        fun set(request: StatisticRequest, response: StatisticResponse) {
            userSession = UserSession(userSession?.username ?: "default", request, response)
        }

        fun clear() {
            userSession = EMPTY_SESSION
        }
    }
}

fun Application.configureSecurity() {
//    install(Sessions) {
//        cookie<UserSession>("user_session")
//    }
}

/*
предполагалось использовать плагин install(Authentication)
но я не смог до конца с ним разобраться, поэтому взял оттуда только валидацию и ручками проверяю
*/
fun validate(username: String, password: String): UserIdPrincipal? =
    hashedUserTable.authenticate(UserPasswordCredential(username, password))

