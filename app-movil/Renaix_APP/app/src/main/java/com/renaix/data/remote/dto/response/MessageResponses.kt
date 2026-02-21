package com.renaix.data.remote.dto.response

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * Respuesta de mensaje
 */
@Serializable
data class MessageResponse(
    val id: Int,
    val texto: String,
    val emisor: OwnerResponse,
    val receptor: OwnerResponse,
    val leido: Boolean = false,
    val fecha: String? = null,
    @SerialName("hilo_id")
    val hiloId: String? = null,
    @SerialName("message_type")
    val messageType: String = "text",
    @SerialName("offer_data")
    val offerData: OfferDataResponse? = null
)

/**
 * Datos de oferta incluidos en mensajes de tipo oferta
 */
@Serializable
data class OfferDataResponse(
    @SerialName("product_id")
    val productId: Int?,
    @SerialName("product_name")
    val productName: String,
    @SerialName("original_price")
    val originalPrice: Double,
    @SerialName("offered_price")
    val offeredPrice: Double
)

/**
 * Respuesta de conversación
 */
@Serializable
data class ConversationResponse(
    @SerialName("hilo_id")
    val hiloId: String,
    val participantes: List<OwnerResponse> = emptyList(),
    @SerialName("ultimo_mensaje")
    val ultimoMensaje: LastMessageResponse? = null,
    val mensajes: List<MessageResponse> = emptyList(),
    @SerialName("total_mensajes")
    val totalMensajes: Int = 0,
    @SerialName("mensajes_no_leidos")
    val mensajesNoLeidos: Int = 0
)

/**
 * Último mensaje en conversación
 */
@Serializable
data class LastMessageResponse(
    val texto: String,
    val fecha: String? = null
)

/**
 * Respuesta de mensajes no leídos
 */
@Serializable
data class UnreadMessagesResponse(
    val total: Int,
    val mensajes: List<MessageResponse>
)

/**
 * Respuesta al aceptar una oferta (incluye mensaje y compra creada)
 */
@Serializable
data class AcceptOfferResponse(
    val mensaje: MessageResponse,
    val compra: PurchaseResponse
)
