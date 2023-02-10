package pages

import api.deleteHistoryResponse
import api.loadHistory
import api.loadHistoryResponse
import api.saveResult
import kotlinx.coroutines.launch
import react.*
import react.dom.html.AnchorTarget
import react.dom.html.ButtonType
import react.dom.html.ImgLoading
import react.dom.html.ReactHTML
import react.dom.html.ReactHTML.br
import react.dom.html.ReactHTML.button
import react.dom.html.ReactHTML.div
import react.dom.html.ReactHTML.h2
import react.dom.html.ReactHTML.li
import react.dom.html.ReactHTML.ol
import react.dom.html.ReactHTML.ul
import react.dom.render
import ru.diamant.rabbit.common.model.HistoryResponse
import ru.diamant.rabbit.common.model.StatisticResponse
import utils.withPreventDefault

external interface HistoryProps : Props {
    var onContentChange: (HistoryResponse) -> Unit
    var onRequestChange: (StatisticResponse) -> Unit
    var onLoadStart: () -> Unit
    var onResponseLoadStart: () -> Unit
}

val HistoryPage = FC<HistoryProps> { props ->
    var currentContent: HistoryResponse? by useState(DEFAULT_STATE)
    var currentResponse: StatisticResponse? by useState(DEFAULT_STATE)

    props.onContentChange = { content ->
        currentContent = content
    }
    props.onRequestChange = { content ->
        currentResponse = content
    }
    props.onLoadStart = {
        currentContent = DEFAULT_STATE
    }
    props.onResponseLoadStart = {
        currentResponse = DEFAULT_STATE
    }
    div {
        h2 { +"History" }
        id = "historyButtonBasket"
        button {
            id = "commonButton"
            type = ButtonType.submit
            onClick = withPreventDefault {
                ApplicationScope.launch {
                    props.onLoadStart()
                    val response: HistoryResponse = loadHistory()
                    props.onContentChange(response)
                }
            }
            +"Load History"
        }

    }
    div {
        id = "HistoryForm"
        if (currentContent?.response?.size ?: 0 > 0) {
            ul {
                for (request in currentContent?.response ?: emptyList()) {
                    li {
                        id = "historyElement"
                        +"url: ${request.url}"
                        br()
                        +"level: ${request.level}"
                        div {

                            button {
                                id = "commonButton"
                                type = ButtonType.submit

                                onClick = withPreventDefault {
                                    ApplicationScope.launch {
                                        props.onResponseLoadStart()
                                        val response: StatisticResponse = loadHistoryResponse(request)
                                        props.onRequestChange(response)
                                    }
                                }
                                +"Show statistic"
                            }

                            button {
                                id = "commonButton"
                                type = ButtonType.submit

                                onClick = withPreventDefault {
                                    ApplicationScope.launch {
                                        props.onLoadStart()
                                        deleteHistoryResponse(request)
                                        val response: HistoryResponse = loadHistory()
                                        props.onContentChange(response)
                                    }
                                }
                                +"Delete"
                            }
                        }
                    }
                }
            }
        }
    }
    Response {
        content = currentResponse
    }

}
