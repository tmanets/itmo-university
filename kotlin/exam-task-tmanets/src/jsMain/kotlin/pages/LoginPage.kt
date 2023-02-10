package pages

import ApplicationScope
import api.getStatistic
import kotlinx.coroutines.launch
import react.FC
import react.Props
import react.dom.html.*
import react.dom.html.ReactHTML.button
import react.dom.html.ReactHTML.div
import react.dom.html.ReactHTML.form
import react.dom.html.ReactHTML.h2
import react.dom.html.ReactHTML.input
import react.dom.html.ReactHTML.p
import react.router.useNavigate
import ru.diamant.rabbit.common.model.StatisticRequest
import ru.diamant.rabbit.common.model.StatisticResponse
import security.UserCredentials
import security.useAuth
import utils.withPreventDefault


val LoginPage = FC<Props> {
    val login = useAuth()::login
    val navigate = useNavigate()
    var username = ""
    var password = ""

    form {
        div {
            id = "commonForm"
            h2 { +"Login" }
            input {
                id = "commonInput"
                type = InputType.text
                name = "username"
                placeholder = "username"
                onChange = { event ->
                    username = event.target.value
                }
            }

            input {
                id = "passInput"
                type = InputType.password
                name = "password"
                placeholder = "password"
                onChange = { event ->
                    password = event.target.value
                }
            }
            button {
                id = "commonButton"
                type = ButtonType.submit
                value = "Login"
                onClick = withPreventDefault {
                    ApplicationScope.launch { login(UserCredentials(username, password)) }
                    navigate("/")
                }
                +"Log in"
            }
        }
    }

}