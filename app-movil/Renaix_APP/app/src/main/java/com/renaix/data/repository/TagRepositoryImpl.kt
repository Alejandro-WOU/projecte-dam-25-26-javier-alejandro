package com.renaix.data.repository

import com.renaix.data.mapper.toDomain
import com.renaix.data.remote.datasource.NetworkResult
import com.renaix.data.remote.datasource.TagRemoteDataSource
import com.renaix.domain.model.Tag
import com.renaix.domain.repository.TagRepository

class TagRepositoryImpl(
    private val remoteDataSource: TagRemoteDataSource
) : TagRepository {

    override suspend fun getPopularTags(): Result<List<Tag>> {
        return when (val result = remoteDataSource.getPopularTags()) {
            is NetworkResult.Success -> Result.success(result.data.map { it.toDomain() })
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }

    override suspend fun createTag(nombre: String): Result<Tag> {
        return when (val result = remoteDataSource.createTag(nombre)) {
            is NetworkResult.Success -> Result.success(result.data.toDomain())
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }

    override suspend fun searchTags(query: String): Result<List<Tag>> {
        return when (val result = remoteDataSource.searchTags(query)) {
            is NetworkResult.Success -> Result.success(result.data.map { it.toDomain() })
            is NetworkResult.Error -> Result.failure(Exception(result.message))
        }
    }
}
