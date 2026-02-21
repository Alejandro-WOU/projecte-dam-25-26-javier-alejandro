package com.renaix.presentation.screens.products.detail

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.renaix.domain.model.ProductDetail
import com.renaix.domain.repository.ProductRepository
import com.renaix.domain.repository.PurchaseRepository
import com.renaix.presentation.common.state.UiState
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class ProductDetailViewModel(
    private val productRepository: ProductRepository,
    private val purchaseRepository: PurchaseRepository
) : ViewModel() {

    private val _state = MutableStateFlow<UiState<ProductDetail>>(UiState.Loading)
    val state: StateFlow<UiState<ProductDetail>> = _state.asStateFlow()

    private val _buyState = MutableStateFlow<UiState<Unit>>(UiState.Idle)
    val buyState: StateFlow<UiState<Unit>> = _buyState.asStateFlow()

    private val _isFavorite = MutableStateFlow(false)
    val isFavorite: StateFlow<Boolean> = _isFavorite.asStateFlow()

    private var currentProductId: Int = -1

    fun loadProduct(productId: Int) {
        currentProductId = productId
        viewModelScope.launch {
            _state.value = UiState.Loading

            // Cargar estado de favorito
            _isFavorite.value = productRepository.isFavorite(productId)

            productRepository.getProductDetail(productId)
                .onSuccess { product ->
                    _state.value = UiState.Success(product)
                }
                .onFailure { exception ->
                    _state.value = UiState.Error(exception.message ?: "Error al cargar producto")
                }
        }
    }

    fun toggleFavorite() {
        if (currentProductId < 0) return
        viewModelScope.launch {
            if (_isFavorite.value) {
                productRepository.removeFromFavorites(currentProductId)
                _isFavorite.value = false
            } else {
                productRepository.addToFavorites(currentProductId)
                _isFavorite.value = true
            }
        }
    }

    fun buyProduct(productId: Int, notas: String? = null) {
        viewModelScope.launch {
            _buyState.value = UiState.Loading

            purchaseRepository.createPurchase(productId, notas)
                .onSuccess {
                    _buyState.value = UiState.Success(Unit)
                }
                .onFailure { exception ->
                    _buyState.value = UiState.Error(exception.message ?: "Error al comprar")
                }
        }
    }

    fun resetBuyState() {
        _buyState.value = UiState.Idle
    }
}
