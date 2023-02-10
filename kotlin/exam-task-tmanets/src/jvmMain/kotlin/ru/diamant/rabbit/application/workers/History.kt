package ru.diamant.rabbit.application.workers

import org.litote.kmongo.reactivestreams.*
import org.litote.kmongo.coroutine.*
import org.litote.kmongo.eq
import ru.diamant.rabbit.application.model.Image
import ru.diamant.rabbit.application.model.Response
import ru.diamant.rabbit.common.model.HistoryResponse
import ru.diamant.rabbit.common.model.StatisticRequest
import ru.diamant.rabbit.common.model.StatisticResponse

class History {
    companion object {
        private val client = KMongo.createClient().coroutine
        private val database = client.getDatabase("history")
        private val imageCol = database.getCollection<Image>()
        private val responseCol = database.getCollection<Response>()

        suspend fun save(user: String, request: StatisticRequest?, response: StatisticResponse?) {
            println("saving $request $response")
            if (request == null || response == null) return //Зато не вызов с !!

            val images: MutableList<Int> = mutableListOf()
            response.images.forEach {
                val imageId = it.hashCode()
                val image = imageCol.findOne(Image::id eq imageId)
                if (image == null) {
                    imageCol.insertOne(Image(it))
                }
                images += imageId
            }

            responseCol.insertOne(Response(user, request, response.topWorlds, images))
        }

        suspend fun getResponse(user: String, request: StatisticRequest): StatisticResponse {

            val data = responseCol.findOne(Response::user eq user, Response::request eq request)
                ?: return StatisticResponse(emptyList(), emptySet())

            val images = data.images.map {
                imageCol.findOne(Image::id eq it)?.url ?: ""
            }.toSet()

            return StatisticResponse(data.words, images)
        }

        suspend fun getRequests(user: String) =
            HistoryResponse(responseCol.find(Response::user eq user).toList().map { it.request })

        suspend fun deleteResponse(user: String, request: StatisticRequest) =
            responseCol.deleteOne(Response::user eq user, Response::request eq request)
    }
}