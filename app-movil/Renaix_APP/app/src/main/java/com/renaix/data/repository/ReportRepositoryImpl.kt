package com.renaix.data.repository

import com.renaix.data.mapper.toDomain
import com.renaix.data.remote.datasource.NetworkResult
import com.renaix.data.remote.datasource.ReportRemoteDataSource
import com.renaix.domain.model.CategoriaDenuncia
import com.renaix.domain.model.Report
import com.renaix.domain.model.TipoDenuncia
import com.renaix.domain.repository.ReportRepository

class ReportRepositoryImpl(
    private val remoteDataSource: ReportRemoteDataSource
) : ReportRepository {

    override suspend fun createReport(
        tipo: TipoDenuncia,
        motivo: String,
        categoria: CategoriaDenuncia,
        productoId: Int?,
        comentarioId: Int?,
        usuarioReportadoId: Int?
    ): Result<Report> {
        return when (val result = remoteDataSource.createReport(
            tipo = tipo.value,
            motivo = motivo,
            categoria = categoria.value,
            productoId = productoId,
            comentarioId = comentarioId,
            usuarioReportadoId = usuarioReportadoId
        )) {
            is NetworkResult.Success -> Result.success(result.data.toDomain())
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }

    override suspend fun getMyReports(): Result<List<Report>> {
        return when (val result = remoteDataSource.getMyReports()) {
            is NetworkResult.Success -> Result.success(result.data.map { it.toDomain() })
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }
}
