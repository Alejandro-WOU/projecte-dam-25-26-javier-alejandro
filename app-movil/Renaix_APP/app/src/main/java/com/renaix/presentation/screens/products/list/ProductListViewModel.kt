package com.renaix.presentation.screens.products.list

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.renaix.domain.model.Product
import com.renaix.domain.repository.ProductRepository
import com.renaix.presentation.common.state.PaginatedState
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class ProductListViewModel(
    private val productRepository: ProductRepository
) : ViewModel() {

    private val _state = MutableStateFlow(PaginatedState<Product>())
    val state: StateFlow<PaginatedState<Product>> = _state.asStateFlow()

    private val _favorites = MutableStateFlow<Set<Int>>(emptySet())
    val favorites: StateFlow<Set<Int>> = _favorites.asStateFlow()

    init {
        loadProducts()
        loadFavorites()
    }

    private fun loadFavorites() {
        viewModelScope.launch {
            productRepository.getFavorites().collect { favoriteProducts ->
                _favorites.value = favoriteProducts.map { it.id }.toSet()
            }
        }
    }

    fun toggleFavorite(productId: Int) {
        viewModelScope.launch {
            if (_favorites.value.contains(productId)) {
                productRepository.removeFromFavorites(productId)
                _favorites.value = _favorites.value - productId
            } else {
                productRepository.addToFavorites(productId)
                _favorites.value = _favorites.value + productId
            }
        }
    }

    fun loadProducts() {
        if (_state.value.isLoading) return

        viewModelScope.launch {
            _state.value = _state.value.copy(isLoading = true, error = null)

            productRepository.getProducts(page = 1)
                .onSuccess { products ->
                    _state.value = _state.value.copy(
                        items = products,
                        isLoading = false,
                        page = 1,
                        hasMore = products.size >= 20,
                        endReached = products.size < 20
                    )
                }
                .onFailure { exception ->
                    _state.value = _state.value.copy(
                        isLoading = false,
                        error = exception.message ?: "Error al cargar productos"
                    )
                }
        }
    }

    fun loadMore() {
        if (_state.value.isLoading || _state.value.endReached) return

        viewModelScope.launch {
            _state.value = _state.value.copy(isLoading = true)

            val nextPage = _state.value.page + 1
            productRepository.getProducts(page = nextPage)
                .onSuccess { products ->
                    _state.value = _state.value.copy(
                        items = _state.value.items + products,
                        isLoading = false,
                        page = nextPage,
                        hasMore = products.size >= 20,
                        endReached = products.size < 20
                    )
                }
                .onFailure { exception ->
                    _state.value = _state.value.copy(
                        isLoading = false,
                        error = exception.message
                    )
                }
        }
    }

    fun refresh() {
        viewModelScope.launch {
            _state.value = _state.value.copy(isRefreshing = true, error = null)

            productRepository.getProducts(page = 1)
                .onSuccess { products ->
                    _state.value = PaginatedState(
                        items = products,
                        isRefreshing = false,
                        page = 1,
                        hasMore = products.size >= 20,
                        endReached = products.size < 20
                    )
                }
                .onFailure { exception ->
                    _state.value = _state.value.copy(
                        isRefreshing = false,
                        error = exception.message
                    )
                }
        }
    }

    fun clearError() {
        _state.value = _state.value.copy(error = null)
    }
}
