package com.renaix.data.remote.dto.response

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * Respuesta de categoría
 */
@Serializable
data class CategoryResponse(
    val id: Int,
    @SerialName("nombre")
    val name: String,
    val descripcion: String? = null,
    @SerialName("imagen_url")
    val imagenUrl: String? = null,
    @SerialName("producto_count")
    val productoCount: Int = 0
)
