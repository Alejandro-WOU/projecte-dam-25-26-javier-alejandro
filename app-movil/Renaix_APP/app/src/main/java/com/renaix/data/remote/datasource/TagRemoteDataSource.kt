package com.renaix.data.remote.datasource

import com.renaix.data.remote.api.RenaixApi
import com.renaix.data.remote.dto.request.CreateTagRequest
import com.renaix.data.remote.dto.response.TagResponse

class TagRemoteDataSource(private val api: RenaixApi) {

    suspend fun getPopularTags(): NetworkResult<List<TagResponse>> {
        return try {
            val response = api.getPopularTags()
            if (response.success && response.data != null) {
                NetworkResult.Success(response.data)
            } else {
                NetworkResult.Error(message = response.error ?: "Error al obtener etiquetas", code = response.code)
            }
        } catch (e: Exception) {
            NetworkResult.Error(message = e.message ?: "Error de conexión", exception = e)
        }
    }

    suspend fun createTag(nombre: String): NetworkResult<TagResponse> {
        return try {
            val response = api.createTag(CreateTagRequest(nombre))
            if (response.success && response.data != null) {
                NetworkResult.Success(response.data)
            } else {
                NetworkResult.Error(message = response.error ?: "Error al crear etiqueta", code = response.code)
            }
        } catch (e: Exception) {
            NetworkResult.Error(message = e.message ?: "Error de conexión", exception = e)
        }
    }

    suspend fun searchTags(query: String): NetworkResult<List<TagResponse>> {
        return try {
            val response = api.searchTags(query)
            if (response.success && response.data != null) {
                NetworkResult.Success(response.data)
            } else {
                NetworkResult.Error(message = response.error ?: "Error al buscar etiquetas", code = response.code)
            }
        } catch (e: Exception) {
            NetworkResult.Error(message = e.message ?: "Error de conexión", exception = e)
        }
    }
}
