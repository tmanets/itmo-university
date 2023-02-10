package pages

import api.getStatistic
import api.saveResult
import kotlinx.coroutines.launch
import react.FC
import react.Props
import react.create
import react.dom.html.*
import react.dom.html.ReactHTML.a
import react.dom.html.ReactHTML.form
import react.dom.html.ReactHTML.ol
import react.dom.html.ReactHTML.input
import react.dom.html.ReactHTML.h2
import react.dom.html.ReactHTML.div
import react.dom.html.ReactHTML.img
import react.dom.html.ReactHTML.button
import react.dom.html.ReactHTML.h3
import react.dom.html.ReactHTML.li
import react.dom.html.ReactHTML.p
import react.dom.render
import react.useState
import ru.diamant.rabbit.common.model.StatisticRequest
import ru.diamant.rabbit.common.model.StatisticResponse
import security.useAuth
import utils.Resource
import utils.withPreventDefault

external interface StatisticFormProps : Props {
    var onContentChange: (StatisticResponse) -> Unit
    var onLoadStart: () -> Unit
}

var targetUrl = ""
var level = 0

val HomePage = FC<StatisticFormProps> { props ->
    var currentContent: StatisticResponse? by useState(DEFAULT_STATE)
    var isLoading: Boolean by useState(false)
    props.onContentChange = { content ->
        currentContent = content
        isLoading = false
    }

    props.onLoadStart = {
        currentContent = DEFAULT_STATE
        isLoading = true
    }
    form {
        div {
            h2 { +"Imaging" }
            id = "commonForm"
            input {
                id = "commonInput"
                type = InputType.url
                name = "url"
                placeholder = "url"
                onChange = { event ->
                    targetUrl = event.target.value
                }
            }

            input {
                id = "commonInput"
                name = "level"
                placeholder = "level"
                onChange = { event ->
                    level = event.target.value.toInt()
                }
            }
            button {
                id = "commonButton"
                type = ButtonType.submit
                onClick = withPreventDefault {
                    ApplicationScope.launch {
                        props.onLoadStart()
                        val response: StatisticResponse = getStatistic(StatisticRequest(targetUrl, level))
                        props.onContentChange(response)

                    }

                }

                +"Imaging!"
            }
        }
    }
    if (isLoading) {
        h2 {
            +"Loading..."
        }
    } else {
        Response {
            content = currentContent
        }
    }
}

