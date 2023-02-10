package ru.diamant.rabbit.application.workers

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.sync.*
import kotlinx.coroutines.withContext
import ru.diamant.rabbit.common.model.StatisticRequest
import ru.diamant.rabbit.common.model.StatisticResponse
import org.jsoup.Jsoup
import java.lang.Integer.min
import kotlin.math.log10


const val MIN_LEVEL = 1
const val MIN_WORD_LENGTH = 5
const val NUMBER_OF_WORDS = 5

// Класс собирающий и хранящий всю статистику с конкретной страницы
class Page(private val url: String, val level: Int) {
    val imageUrls: MutableSet<String> = mutableSetOf()
    val pageUrls: MutableSet<String> = mutableSetOf()
    val wordOccurrence: MutableMap<String, Double> = mutableMapOf()

    private fun weight(occurrence: Double): Double {
        return occurrence * level * (1 - log10(1.0 + level))
    }

    fun parse() {
        println("parsing url: $url, level: $level")

        val document = Jsoup.connect(url).get()
        imageUrls.addAll(document.getElementsByTag("img").map { it.attr("abs:src") })
        pageUrls.addAll(document.getElementsByTag("a").map { it.attr("abs:href") })
        document.text()
            .split("\\s".toRegex())
            .map { it.lowercase() }
            .filter { it.length >= MIN_WORD_LENGTH && it.all(Char::isLetter) }
            .forEach {
                wordOccurrence.merge(it, 1.0, Double::plus)
            }
        wordOccurrence.mapValues { weight(it.value) }

        println("page parsed successfully: $url")
    }

}


// Класс, из которого мы запускаем корутины и формируем ответ
class StatisticWorker(private val maxLevel: Int) {
    private var linksMutex = Mutex()
    private var pagesMutex = Mutex()
    private val visitedLinks: MutableMap<String, Int> = mutableMapOf()
    private val images: MutableSet<String> = mutableSetOf()
    private val pages: MutableMap<String, Page> = mutableMapOf()

    suspend fun process(url: String, currentLevel: Int) {
        if (currentLevel > maxLevel) return
        if (visitedLinks.getOrDefault(url, -1) >= currentLevel) return
        linksMutex.withLock {
            visitedLinks[url] = currentLevel
        }

        runCatching {
            withContext(Dispatchers.Default) {
                coroutineScope {
                    val page = Page(url, currentLevel).apply { parse() }
                    pagesMutex.withLock {
                        if ((pages[url]?.level ?: Int.MAX_VALUE) > currentLevel) {
                            pages[url] = page
                        }
                    }
                    page.pageUrls.forEach {
                        launch { process(it, currentLevel + 1) }
                    }
                }
            }
        }

    }

    fun response(): StatisticResponse {
        pages.values.forEach {
            images.addAll(it.imageUrls)
        }
        val words: MutableMap<String, Double> = mutableMapOf()
        pages.values.forEach {
            it.wordOccurrence.forEach { (key, value) ->
                words.merge(key, value, Double::plus)
            }
        }
        val topWords = words.toList()
            .sortedByDescending { it.second }
            .map { it.first }
            .take(min(NUMBER_OF_WORDS, words.size))

        return StatisticResponse(topWords, images)
    }
}

suspend fun processStatistic(request: StatisticRequest): StatisticResponse {
    val worker = StatisticWorker(request.level)
    worker.process(request.url, MIN_LEVEL)
    return worker.response()
}
