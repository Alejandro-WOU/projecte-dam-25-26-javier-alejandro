package com.renaix.data.remote.datasource

import com.renaix.data.remote.api.RenaixApi
import com.renaix.data.remote.dto.request.CreateReportRequest
import com.renaix.data.remote.dto.response.ReportResponse

class ReportRemoteDataSource(private val api: RenaixApi) {

    suspend fun createReport(
        tipo: String,
        motivo: String,
        categoria: String,
        productoId: Int? = null,
        comentarioId: Int? = null,
        usuarioReportadoId: Int? = null
    ): NetworkResult<ReportResponse> {
        return try {
            val response = api.createReport(
                CreateReportRequest(
                    tipo = tipo,
                    motivo = motivo,
                    categoria = categoria,
                    productoId = productoId,
                    comentarioId = comentarioId,
                    usuarioReportadoId = usuarioReportadoId
                )
            )
            if (response.success && response.data != null) {
                NetworkResult.Success(response.data)
            } else {
                NetworkResult.Error(message = response.error ?: "Error al crear denuncia", code = response.code)
            }
        } catch (e: Exception) {
            NetworkResult.Error(message = e.message ?: "Error de conexión", exception = e)
        }
    }

    suspend fun getMyReports(): NetworkResult<List<ReportResponse>> {
        return try {
            val response = api.getMyReports()
            if (response.success && response.data != null) {
                NetworkResult.Success(response.data)
            } else {
                NetworkResult.Error(message = response.error ?: "Error al obtener denuncias", code = response.code)
            }
        } catch (e: Exception) {
            NetworkResult.Error(message = e.message ?: "Error de conexión", exception = e)
        }
    }
}
