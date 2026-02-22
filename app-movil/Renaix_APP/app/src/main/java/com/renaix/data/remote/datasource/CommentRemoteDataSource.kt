package com.renaix.data.remote.datasource

import com.renaix.data.remote.api.RenaixApi
import com.renaix.data.remote.dto.request.CreateCommentRequest
import com.renaix.data.remote.dto.response.CommentResponse

class CommentRemoteDataSource(private val api: RenaixApi) {

    suspend fun createComment(productId: Int, texto: String): NetworkResult<CommentResponse> {
        return try {
            val response = api.createComment(productId, CreateCommentRequest(texto))
            if (response.success && response.data != null) {
                NetworkResult.Success(response.data)
            } else {
                NetworkResult.Error(message = response.error ?: "Error al crear comentario", code = response.code)
            }
        } catch (e: Exception) {
            NetworkResult.Error(message = e.message ?: "Error de conexión", exception = e)
        }
    }

    suspend fun deleteComment(commentId: Int): NetworkResult<Unit> {
        return try {
            val response = api.deleteComment(commentId)
            if (response.success) {
                NetworkResult.Success(Unit)
            } else {
                NetworkResult.Error(message = response.error ?: "Error al eliminar comentario", code = response.code)
            }
        } catch (e: Exception) {
            NetworkResult.Error(message = e.message ?: "Error de conexión", exception = e)
        }
    }
}
