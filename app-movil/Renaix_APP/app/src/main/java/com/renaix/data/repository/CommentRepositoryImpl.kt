package com.renaix.data.repository

import com.renaix.data.mapper.toDomain
import com.renaix.data.remote.datasource.CommentRemoteDataSource
import com.renaix.data.remote.datasource.NetworkResult
import com.renaix.domain.model.Comment
import com.renaix.domain.repository.CommentRepository

class CommentRepositoryImpl(
    private val remoteDataSource: CommentRemoteDataSource
) : CommentRepository {

    override suspend fun createComment(productId: Int, texto: String): Result<Comment> {
        return when (val result = remoteDataSource.createComment(productId, texto)) {
            is NetworkResult.Success -> Result.success(result.data.toDomain())
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }

    override suspend fun deleteComment(commentId: Int): Result<Unit> {
        return when (val result = remoteDataSource.deleteComment(commentId)) {
            is NetworkResult.Success -> Result.success(Unit)
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }
}
