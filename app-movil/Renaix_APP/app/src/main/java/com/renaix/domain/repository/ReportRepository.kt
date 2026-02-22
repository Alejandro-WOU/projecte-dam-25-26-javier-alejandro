package com.renaix.domain.repository

import com.renaix.domain.model.CategoriaDenuncia
import com.renaix.domain.model.Report
import com.renaix.domain.model.TipoDenuncia

interface ReportRepository {
    suspend fun createReport(
        tipo: TipoDenuncia,
        motivo: String,
        categoria: CategoriaDenuncia,
        productoId: Int? = null,
        comentarioId: Int? = null,
        usuarioReportadoId: Int? = null
    ): Result<Report>

    suspend fun getMyReports(): Result<List<Report>>
}
