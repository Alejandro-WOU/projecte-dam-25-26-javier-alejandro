package com.renaix.domain.model

/**
 * Tipos de mensajes soportados en el chat
 */
enum class MessageType {
    /** Mensaje de texto normal */
    TEXT,
    /** Oferta de precio propuesta por el comprador */
    OFFER,
    /** Confirmación de que la oferta fue aceptada */
    OFFER_ACCEPTED,
    /** Notificación de que la oferta fue rechazada */
    OFFER_REJECTED,
    /** Contraoferta propuesta por el vendedor */
    COUNTER_OFFER;

    companion object {
        fun fromString(value: String): MessageType {
            return when (value.lowercase()) {
                "text" -> TEXT
                "offer" -> OFFER
                "offer_accepted" -> OFFER_ACCEPTED
                "offer_rejected" -> OFFER_REJECTED
                "counter_offer" -> COUNTER_OFFER
                else -> TEXT
            }
        }
    }
}

/**
 * Datos asociados a una oferta de compra
 */
data class OfferData(
    val productId: Int,
    val productName: String,
    val originalPrice: Double,
    val offeredPrice: Double
)

/**
 * Modelo de dominio para Mensaje
 * Soporta mensajes de texto normales y mensajes especiales de ofertas
 */
data class Message(
    val id: Int,
    val texto: String,
    val emisor: Owner,
    val receptor: Owner,
    val leido: Boolean = false,
    val fecha: String? = null,
    val hiloId: String? = null,
    /** Tipo de mensaje (texto, oferta, etc.) */
    val messageType: MessageType = MessageType.TEXT,
    /** Datos de la oferta (solo si messageType es OFFER/OFFER_ACCEPTED/OFFER_REJECTED/COUNTER_OFFER) */
    val offerData: OfferData? = null
)

/**
 * Modelo de dominio para Conversación
 */
data class Conversation(
    val hiloId: String,
    val participantes: List<Owner>,
    val ultimoMensaje: LastMessage? = null,
    val mensajes: List<Message> = emptyList()
) {
    /**
     * Obtiene el otro participante de la conversación
     */
    fun getOtherParticipant(currentUserId: Int): Owner? {
        return participantes.find { it.id != currentUserId }
    }
}

/**
 * Último mensaje de una conversación
 */
data class LastMessage(
    val texto: String,
    val fecha: String? = null
)

/**
 * Mensajes no leídos
 */
data class UnreadMessages(
    val total: Int,
    val mensajes: List<Message>
)
