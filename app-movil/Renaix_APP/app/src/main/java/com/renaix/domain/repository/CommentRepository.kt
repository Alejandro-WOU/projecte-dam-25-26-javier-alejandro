package com.renaix.domain.repository

import com.renaix.domain.model.Comment

interface CommentRepository {
    suspend fun createComment(productId: Int, texto: String): Result<Comment>
    suspend fun deleteComment(commentId: Int): Result<Unit>
}
