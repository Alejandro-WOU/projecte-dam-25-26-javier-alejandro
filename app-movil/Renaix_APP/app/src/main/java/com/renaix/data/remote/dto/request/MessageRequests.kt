package com.renaix.data.remote.dto.request

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * Request para enviar un mensaje
 */
@Serializable
data class SendMessageRequest(
    @SerialName("receptor_id")
    val receptorId: Int,
    val texto: String,
    @SerialName("producto_id")
    val productoId: Int? = null
)

/**
 * Request para enviar una oferta de precio
 */
@Serializable
data class SendOfferRequest(
    @SerialName("producto_id")
    val productoId: Int,
    @SerialName("precio_ofertado")
    val precioOfertado: Double
)

/**
 * Request para enviar una contraoferta
 */
@Serializable
data class SendCounterOfferRequest(
    @SerialName("oferta_id")
    val ofertaId: Int,
    @SerialName("precio_contraoferta")
    val precioContraoferta: Double
)
