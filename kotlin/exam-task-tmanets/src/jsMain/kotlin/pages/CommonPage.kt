package pages

import api.saveResult
import components.AuthStatus
import kotlinx.coroutines.launch
import react.FC
import react.Props
import react.dom.html.AnchorTarget
import react.dom.html.ButtonType
import react.dom.html.ImgLoading
import react.dom.html.ReactHTML
import react.dom.html.ReactHTML.a
import react.dom.html.ReactHTML.button
import react.dom.html.ReactHTML.div
import react.dom.html.ReactHTML.h3
import react.dom.html.ReactHTML.img
import react.dom.html.ReactHTML.li
import react.dom.html.ReactHTML.ol
import react.dom.html.ReactHTML.ul
import react.key
import react.router.Outlet
import react.router.dom.Link
import react.useState
import ru.diamant.rabbit.common.model.StatisticResponse
import security.useAuth
import utils.Resource
import utils.withPreventDefault

val DEFAULT_STATE = null

external interface CommonPageProps : Props {
    var menuItems: Map<String, String>
}

external interface ResponseProps : Props {
    var content: StatisticResponse?
}

val Response = FC<ResponseProps> { props ->
    val content: StatisticResponse? = props.content

    if (content != DEFAULT_STATE) {
        div {
            id = "responseForm"

            if (content != DEFAULT_STATE && useAuth().user is Resource.Ok) {
                div {
                    id = "saveButton"
                    button {
                        id = "commonButton"
                        type = ButtonType.submit
                        onClick = withPreventDefault {
                            ApplicationScope.launch {
                                saveResult()
                            }
                        }
                        +"Save to favorites"
                    }
                }
            }

            div {
                id = "topWordsBasket"
                if (content.topWorlds.isNotEmpty()) {
                    h3 {
                        +"Top ${content.topWorlds.size} words: "
                    }
                }
                ol {
                    for (word in content.topWorlds) {
                        li {
                            +word
                        }
                    }
                }
            }

            div {
                id = "imageBasket"
                if (content.images.isNotEmpty()) {
                    h3 {
                        +"Images: "
                    }
                }
                for (path in content.images) {
                    a {
                        target = AnchorTarget._blank
                        href = path
                        img {
                            src = path
                            width = 100.0
                            height = 100.0
                            loading = ImgLoading.lazy
                            title = "Click on Image to open it in new tub"
                        }
                    }
                }
            }
        }
    }
}

val CommonPage = FC<CommonPageProps> { props ->
    ReactHTML.nav {
        div {
            id = "menu"
            ul {
                props.menuItems.forEach {
                    li {
                        Link {
                            key = it.key
                            to = it.key
                            +it.value
                        }
                    }
                }
                AuthStatus()
            }
        }
    }


    Outlet()
}
