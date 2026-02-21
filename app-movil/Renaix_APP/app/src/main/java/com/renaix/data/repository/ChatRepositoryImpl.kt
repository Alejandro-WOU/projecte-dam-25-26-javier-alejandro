package com.renaix.data.repository

import com.renaix.data.mapper.toDomain
import com.renaix.data.remote.datasource.ChatRemoteDataSource
import com.renaix.data.remote.datasource.NetworkResult
import com.renaix.domain.model.Conversation
import com.renaix.domain.model.Message
import com.renaix.domain.model.Purchase
import com.renaix.domain.model.UnreadMessages
import com.renaix.domain.repository.ChatRepository

/**
 * Implementación del repositorio de chat
 */
class ChatRepositoryImpl(
    private val remoteDataSource: ChatRemoteDataSource
) : ChatRepository {

    override suspend fun getConversations(): Result<List<Conversation>> {
        return when (val result = remoteDataSource.getConversations()) {
            is NetworkResult.Success -> Result.success(result.data.map { it.toDomain() })
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }

    override suspend fun getConversation(userId: Int, productId: Int?): Result<List<Message>> {
        return when (val result = remoteDataSource.getConversation(userId, productId)) {
            is NetworkResult.Success -> Result.success(result.data.map { it.toDomain() })
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }

    override suspend fun getUnreadMessages(): Result<UnreadMessages> {
        return when (val result = remoteDataSource.getUnreadMessages()) {
            is NetworkResult.Success -> Result.success(result.data.toDomain())
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }

    override suspend fun getUnreadCount(): Result<Int> {
        return when (val result = remoteDataSource.getUnreadMessages()) {
            is NetworkResult.Success -> Result.success(result.data.total)
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }

    override suspend fun sendMessage(
        receptorId: Int,
        texto: String,
        productoId: Int?
    ): Result<Message> {
        return when (val result = remoteDataSource.sendMessage(receptorId, texto, productoId)) {
            is NetworkResult.Success -> Result.success(result.data.toDomain())
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }

    override suspend fun markAsRead(messageId: Int): Result<Unit> {
        return when (val result = remoteDataSource.markAsRead(messageId)) {
            is NetworkResult.Success -> Result.success(Unit)
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }

    // ==================== OFERTAS ====================

    override suspend fun sendOffer(
        productoId: Int,
        precioOfertado: Double
    ): Result<Message> {
        return when (val result = remoteDataSource.sendOffer(productoId, precioOfertado)) {
            is NetworkResult.Success -> Result.success(result.data.toDomain())
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }

    override suspend fun acceptOffer(messageId: Int): Result<Pair<Message, Purchase>> {
        return when (val result = remoteDataSource.acceptOffer(messageId)) {
            is NetworkResult.Success -> {
                val message = result.data.mensaje.toDomain()
                val purchase = result.data.compra.toDomain()
                Result.success(Pair(message, purchase))
            }
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }

    override suspend fun rejectOffer(messageId: Int): Result<Message> {
        return when (val result = remoteDataSource.rejectOffer(messageId)) {
            is NetworkResult.Success -> Result.success(result.data.toDomain())
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }

    override suspend fun sendCounterOffer(
        ofertaId: Int,
        precioContraoferta: Double
    ): Result<Message> {
        return when (val result = remoteDataSource.sendCounterOffer(ofertaId, precioContraoferta)) {
            is NetworkResult.Success -> Result.success(result.data.toDomain())
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }
}
