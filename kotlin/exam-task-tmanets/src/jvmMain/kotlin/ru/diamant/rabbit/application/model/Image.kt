package ru.diamant.rabbit.application.model

data class Image(val url: String) {
    val id: Int = url.hashCode()
    // наверное лучше картинку хэшировать, а не url
}
