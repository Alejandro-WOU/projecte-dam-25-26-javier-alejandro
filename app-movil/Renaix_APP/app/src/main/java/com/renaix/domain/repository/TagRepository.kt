package com.renaix.domain.repository

import com.renaix.domain.model.Tag

interface TagRepository {
    suspend fun getPopularTags(): Result<List<Tag>>
    suspend fun createTag(nombre: String): Result<Tag>
    suspend fun searchTags(query: String): Result<List<Tag>>
}
