package com.renaix.domain.repository

import com.renaix.domain.model.Conversation
import com.renaix.domain.model.Message
import com.renaix.domain.model.Purchase
import com.renaix.domain.model.UnreadMessages

/**
 * Repositorio de chat/mensajería
 */
interface ChatRepository {
    /**
     * Obtiene lista de conversaciones
     */
    suspend fun getConversations(): Result<List<Conversation>>

    /**
     * Obtiene conversación con un usuario
     */
    suspend fun getConversation(
        userId: Int,
        productId: Int? = null
    ): Result<List<Message>>

    /**
     * Obtiene mensajes no leídos
     */
    suspend fun getUnreadMessages(): Result<UnreadMessages>

    /**
     * Obtiene el conteo de mensajes no leídos
     */
    suspend fun getUnreadCount(): Result<Int>

    /**
     * Envía un mensaje
     */
    suspend fun sendMessage(
        receptorId: Int,
        texto: String,
        productoId: Int? = null
    ): Result<Message>

    /**
     * Marca un mensaje como leído
     */
    suspend fun markAsRead(messageId: Int): Result<Unit>

    // ==================== OFERTAS ====================

    /**
     * Envía una oferta de precio sobre un producto
     */
    suspend fun sendOffer(
        productoId: Int,
        precioOfertado: Double
    ): Result<Message>

    /**
     * Acepta una oferta recibida (crea compra con precio negociado)
     */
    suspend fun acceptOffer(messageId: Int): Result<Pair<Message, Purchase>>

    /**
     * Rechaza una oferta recibida
     */
    suspend fun rejectOffer(messageId: Int): Result<Message>

    /**
     * Envía una contraoferta
     */
    suspend fun sendCounterOffer(
        ofertaId: Int,
        precioContraoferta: Double
    ): Result<Message>
}
