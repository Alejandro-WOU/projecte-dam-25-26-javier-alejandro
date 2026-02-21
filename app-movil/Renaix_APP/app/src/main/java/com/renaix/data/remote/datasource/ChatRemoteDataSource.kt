package com.renaix.data.remote.datasource

import com.renaix.data.remote.api.RenaixApi
import com.renaix.data.remote.dto.request.SendCounterOfferRequest
import com.renaix.data.remote.dto.request.SendMessageRequest
import com.renaix.data.remote.dto.request.SendOfferRequest
import com.renaix.data.remote.dto.response.*

/**
 * DataSource remoto para operaciones de chat/mensajería
 */
class ChatRemoteDataSource(private val api: RenaixApi) {

    /**
     * Obtiene lista de conversaciones
     */
    suspend fun getConversations(): NetworkResult<List<ConversationResponse>> {
        return try {
            val response = api.getConversations()

            if (response.success && response.data != null) {
                NetworkResult.Success(response.data)
            } else {
                NetworkResult.Error(
                    message = response.error ?: "Error al obtener conversaciones",
                    code = response.code
                )
            }
        } catch (e: Exception) {
            NetworkResult.Error(
                message = e.message ?: "Error de conexión",
                exception = e
            )
        }
    }

    /**
     * Obtiene conversación con un usuario
     */
    suspend fun getConversation(
        userId: Int,
        productId: Int? = null
    ): NetworkResult<List<MessageResponse>> {
        return try {
            val response = api.getConversation(userId, productId)

            if (response.success && response.data != null) {
                NetworkResult.Success(response.data)
            } else {
                NetworkResult.Error(
                    message = response.error ?: "Error al obtener conversación",
                    code = response.code
                )
            }
        } catch (e: Exception) {
            NetworkResult.Error(
                message = e.message ?: "Error de conexión",
                exception = e
            )
        }
    }

    /**
     * Obtiene mensajes no leídos
     */
    suspend fun getUnreadMessages(): NetworkResult<UnreadMessagesResponse> {
        return try {
            val response = api.getUnreadMessages()

            if (response.success && response.data != null) {
                NetworkResult.Success(response.data)
            } else {
                NetworkResult.Error(
                    message = response.error ?: "Error al obtener mensajes",
                    code = response.code
                )
            }
        } catch (e: Exception) {
            NetworkResult.Error(
                message = e.message ?: "Error de conexión",
                exception = e
            )
        }
    }

    /**
     * Envía un mensaje
     */
    suspend fun sendMessage(
        receptorId: Int,
        texto: String,
        productoId: Int? = null
    ): NetworkResult<MessageResponse> {
        return try {
            val response = api.sendMessage(
                SendMessageRequest(receptorId, texto, productoId)
            )

            if (response.success && response.data != null) {
                NetworkResult.Success(response.data)
            } else {
                NetworkResult.Error(
                    message = response.error ?: "Error al enviar mensaje",
                    code = response.code
                )
            }
        } catch (e: Exception) {
            NetworkResult.Error(
                message = e.message ?: "Error de conexión",
                exception = e
            )
        }
    }

    /**
     * Marca un mensaje como leído
     */
    suspend fun markAsRead(messageId: Int): NetworkResult<Unit> {
        return try {
            val response = api.markMessageAsRead(messageId)

            if (response.success) {
                NetworkResult.Success(Unit)
            } else {
                NetworkResult.Error(
                    message = response.error ?: "Error al marcar mensaje",
                    code = response.code
                )
            }
        } catch (e: Exception) {
            NetworkResult.Error(
                message = e.message ?: "Error de conexión",
                exception = e
            )
        }
    }

    // ==================== OFERTAS ====================

    /**
     * Envía una oferta de precio sobre un producto
     */
    suspend fun sendOffer(
        productoId: Int,
        precioOfertado: Double
    ): NetworkResult<MessageResponse> {
        return try {
            val response = api.sendOffer(
                SendOfferRequest(productoId, precioOfertado)
            )

            if (response.success && response.data != null) {
                NetworkResult.Success(response.data)
            } else {
                NetworkResult.Error(
                    message = response.error ?: "Error al enviar oferta",
                    code = response.code
                )
            }
        } catch (e: Exception) {
            NetworkResult.Error(
                message = e.message ?: "Error de conexión",
                exception = e
            )
        }
    }

    /**
     * Acepta una oferta recibida
     */
    suspend fun acceptOffer(messageId: Int): NetworkResult<AcceptOfferResponse> {
        return try {
            val response = api.acceptOffer(messageId)

            if (response.success && response.data != null) {
                NetworkResult.Success(response.data)
            } else {
                NetworkResult.Error(
                    message = response.error ?: "Error al aceptar oferta",
                    code = response.code
                )
            }
        } catch (e: Exception) {
            NetworkResult.Error(
                message = e.message ?: "Error de conexión",
                exception = e
            )
        }
    }

    /**
     * Rechaza una oferta recibida
     */
    suspend fun rejectOffer(messageId: Int): NetworkResult<MessageResponse> {
        return try {
            val response = api.rejectOffer(messageId)

            if (response.success && response.data != null) {
                NetworkResult.Success(response.data)
            } else {
                NetworkResult.Error(
                    message = response.error ?: "Error al rechazar oferta",
                    code = response.code
                )
            }
        } catch (e: Exception) {
            NetworkResult.Error(
                message = e.message ?: "Error de conexión",
                exception = e
            )
        }
    }

    /**
     * Envía una contraoferta
     */
    suspend fun sendCounterOffer(
        ofertaId: Int,
        precioContraoferta: Double
    ): NetworkResult<MessageResponse> {
        return try {
            val response = api.sendCounterOffer(
                SendCounterOfferRequest(ofertaId, precioContraoferta)
            )

            if (response.success && response.data != null) {
                NetworkResult.Success(response.data)
            } else {
                NetworkResult.Error(
                    message = response.error ?: "Error al enviar contraoferta",
                    code = response.code
                )
            }
        } catch (e: Exception) {
            NetworkResult.Error(
                message = e.message ?: "Error de conexión",
                exception = e
            )
        }
    }
}
