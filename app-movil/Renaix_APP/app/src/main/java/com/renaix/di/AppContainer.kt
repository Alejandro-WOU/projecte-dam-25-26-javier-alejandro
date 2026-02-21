package com.renaix.di

import android.content.Context
import com.renaix.data.local.database.DatabaseDriverFactory
import com.renaix.data.local.database.DatabaseHelper
import com.renaix.data.local.preferences.PreferencesManager
import com.renaix.data.local.preferences.SecurePreferences
import com.renaix.data.remote.api.KtorClient
import com.renaix.data.remote.api.RenaixApi
import com.renaix.data.remote.datasource.AuthRemoteDataSource
import com.renaix.data.remote.datasource.CategoryRemoteDataSource
import com.renaix.data.remote.datasource.ChatRemoteDataSource
import com.renaix.data.remote.datasource.ProductRemoteDataSource
import com.renaix.data.remote.datasource.PurchaseRemoteDataSource
import com.renaix.data.remote.datasource.UserRemoteDataSource
import com.renaix.data.repository.AuthRepositoryImpl
import com.renaix.data.repository.CategoryRepositoryImpl
import com.renaix.data.repository.ChatRepositoryImpl
import com.renaix.data.repository.ProductRepositoryImpl
import com.renaix.data.repository.PurchaseRepositoryImpl
import com.renaix.data.repository.UserRepositoryImpl
import com.renaix.domain.repository.AuthRepository
import com.renaix.domain.repository.CategoryRepository
import com.renaix.domain.repository.ChatRepository
import com.renaix.domain.repository.ProductRepository
import com.renaix.domain.repository.PurchaseRepository
import com.renaix.domain.repository.UserRepository

/**
 * Contenedor de dependencias manual (DI)
 * Arquitectura simplificada: Screen → ViewModel → Repository → API
 */
interface AppContainer {
    val preferencesManager: PreferencesManager
    val authRepository: AuthRepository
    val productRepository: ProductRepository
    val userRepository: UserRepository
    val categoryRepository: CategoryRepository
    val chatRepository: ChatRepository
    val purchaseRepository: PurchaseRepository
}

/**
 * Implementación del contenedor de dependencias
 */
class AppContainerImpl(private val context: Context) : AppContainer {

    // Preferences
    private val securePreferences by lazy {
        SecurePreferences(context)
    }

    override val preferencesManager: PreferencesManager by lazy {
        PreferencesManager(securePreferences)
    }

    // Database
    private val databaseDriverFactory by lazy {
        DatabaseDriverFactory(context)
    }

    private val databaseHelper by lazy {
        DatabaseHelper(databaseDriverFactory)
    }

    private val database by lazy {
        databaseHelper.database
    }

    // Network
    private val publicHttpClient by lazy {
        KtorClient.createPublicClient()
    }

    private val authenticatedHttpClient by lazy {
        KtorClient.createAuthenticatedClient(preferencesManager)
    }

    private val renaixApi by lazy {
        RenaixApi(publicHttpClient, authenticatedHttpClient)
    }

    // Data Sources
    private val authRemoteDataSource by lazy {
        AuthRemoteDataSource(renaixApi)
    }

    private val productRemoteDataSource by lazy {
        ProductRemoteDataSource(renaixApi)
    }

    private val userRemoteDataSource by lazy {
        UserRemoteDataSource(renaixApi)
    }

    private val categoryRemoteDataSource by lazy {
        CategoryRemoteDataSource(renaixApi)
    }

    private val chatRemoteDataSource by lazy {
        ChatRemoteDataSource(renaixApi)
    }

    private val purchaseRemoteDataSource by lazy {
        PurchaseRemoteDataSource(renaixApi)
    }

    // Repositories
    override val authRepository: AuthRepository by lazy {
        AuthRepositoryImpl(authRemoteDataSource, preferencesManager)
    }

    override val productRepository: ProductRepository by lazy {
        ProductRepositoryImpl(productRemoteDataSource, database)
    }

    override val userRepository: UserRepository by lazy {
        UserRepositoryImpl(userRemoteDataSource)
    }

    override val categoryRepository: CategoryRepository by lazy {
        CategoryRepositoryImpl(categoryRemoteDataSource, database)
    }

    override val chatRepository: ChatRepository by lazy {
        ChatRepositoryImpl(chatRemoteDataSource)
    }

    override val purchaseRepository: PurchaseRepository by lazy {
        PurchaseRepositoryImpl(purchaseRemoteDataSource)
    }
}
