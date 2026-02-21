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

    fun loadProduct(productId: Int) {
        viewModelScope.launch {
            _state.value = UiState.Loading

            productRepository.getProductDetail(productId)
                .onSuccess { product ->
                    _state.value = UiState.Success(product)
                }
                .onFailure { exception ->
                    _state.value = UiState.Error(exception.message ?: "Error al cargar producto")
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
