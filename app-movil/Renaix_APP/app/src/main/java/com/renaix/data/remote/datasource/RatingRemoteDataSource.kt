package com.renaix.data.remote.datasource

import com.renaix.data.remote.api.RenaixApi
import com.renaix.data.remote.dto.response.RatingResponse

class RatingRemoteDataSource(private val api: RenaixApi) {

    suspend fun getMyRatings(): NetworkResult<List<RatingResponse>> {
        return try {
            val response = api.getMyRatings()
            if (response.success && response.data != null) {
                NetworkResult.Success(response.data)
            } else {
                NetworkResult.Error(message = response.error ?: "Error al obtener valoraciones", code = response.code)
            }
        } catch (e: Exception) {
            NetworkResult.Error(message = e.message ?: "Error de conexión", exception = e)
        }
    }

    suspend fun getUserRatings(userId: Int): NetworkResult<List<RatingResponse>> {
        return try {
            val response = api.getUserRatings(userId)
            if (response.success && response.data != null) {
                NetworkResult.Success(response.data)
            } else {
                NetworkResult.Error(message = response.error ?: "Error al obtener valoraciones", code = response.code)
            }
        } catch (e: Exception) {
            NetworkResult.Error(message = e.message ?: "Error de conexión", exception = e)
        }
    }
}
