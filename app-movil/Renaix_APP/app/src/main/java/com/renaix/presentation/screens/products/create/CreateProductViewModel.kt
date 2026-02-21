package com.renaix.presentation.screens.products.create

import android.net.Uri
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.renaix.domain.repository.CategoryRepository
import com.renaix.domain.repository.ProductRepository
import com.renaix.presentation.common.state.UiState
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class CreateProductViewModel(
    private val productRepository: ProductRepository,
    private val categoryRepository: CategoryRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<UiState<Int>>(UiState.Idle)
    val uiState: StateFlow<UiState<Int>> = _uiState.asStateFlow()

    private val _formState = MutableStateFlow(CreateProductFormState())
    val formState: StateFlow<CreateProductFormState> = _formState.asStateFlow()

    private val _selectedImages = MutableStateFlow<List<Uri>>(emptyList())
    val selectedImages: StateFlow<List<Uri>> = _selectedImages.asStateFlow()

    init {
        loadCategories()
    }

    private fun loadCategories() {
        viewModelScope.launch {
            categoryRepository.getCategories()
                .onSuccess { categories ->
                    _formState.value = _formState.value.copy(
                        availableCategories = categories
                    )
                }
        }
    }

    /**
     * Actualiza el nombre del producto
     */
    fun updateName(name: String) {
        _formState.value = _formState.value.copy(
            nombre = name,
            nombreError = null
        )
    }

    /**
     * Actualiza la descripción
     */
    fun updateDescription(description: String) {
        _formState.value = _formState.value.copy(
            descripcion = description,
            descripcionError = null
        )
    }

    /**
     * Actualiza el precio
     */
    fun updatePrice(price: String) {
        _formState.value = _formState.value.copy(
            precio = price,
            precioError = null
        )
    }

    /**
     * Selecciona una categoría
     */
    fun selectCategory(categoryId: Int) {
        _formState.value = _formState.value.copy(
            categoriaId = categoryId,
            categoriaError = null
        )
    }

    /**
     * Añade imágenes seleccionadas
     */
    fun addImages(uris: List<Uri>) {
        val currentImages = _selectedImages.value.toMutableList()
        currentImages.addAll(uris)

        // Limitar a 10 imágenes máximo
        _selectedImages.value = currentImages.take(10)
    }

    /**
     * Elimina una imagen
     */
    fun removeImage(uri: Uri) {
        _selectedImages.value = _selectedImages.value.filter { it != uri }
    }

    /**
     * Valida y crea el producto
     */
    fun createProduct() {
        val state = _formState.value

        // Validaciones - acumular todos los errores en una sola copia
        var nombreError: String? = null
        var descripcionError: String? = null
        var precioError: String? = null
        var categoriaError: String? = null

        if (state.nombre.isBlank()) {
            nombreError = "El nombre es obligatorio"
        } else if (state.nombre.length < 3) {
            nombreError = "El nombre debe tener al menos 3 caracteres"
        }

        if (state.descripcion.isBlank()) {
            descripcionError = "La descripción es obligatoria"
        } else if (state.descripcion.length < 10) {
            descripcionError = "La descripción debe tener al menos 10 caracteres"
        }

        val priceValue = state.precio.toDoubleOrNull()
        if (priceValue == null || priceValue <= 0) {
            precioError = "Precio inválido"
        }

        if (state.categoriaId == null) {
            categoriaError = "Selecciona una categoría"
        }

        val hasErrors = nombreError != null || descripcionError != null ||
                precioError != null || categoriaError != null

        if (hasErrors) {
            _formState.value = state.copy(
                nombreError = nombreError,
                descripcionError = descripcionError,
                precioError = precioError,
                categoriaError = categoriaError
            )
            return
        }

        // Crear producto
        viewModelScope.launch {
            _uiState.value = UiState.Loading

            productRepository.createProduct(
                nombre = state.nombre,
                descripcion = state.descripcion,
                precio = priceValue!!,
                categoriaId = state.categoriaId!!,
                estadoProducto = state.estadoProducto,
                antiguedad = state.antiguedad,
                ubicacion = state.ubicacion,
                etiquetaIds = state.etiquetaIds
            ).onSuccess { productId ->
                _uiState.value = UiState.Success(productId)
            }.onFailure { error ->
                _uiState.value = UiState.Error(
                    error.message ?: "Error al crear el producto"
                )
            }
        }
    }

    /**
     * Resetea el estado UI
     */
    fun resetUiState() {
        _uiState.value = UiState.Idle
    }
}

/**
 * Estado del formulario de creación
 */
data class CreateProductFormState(
    val nombre: String = "",
    val nombreError: String? = null,
    val descripcion: String = "",
    val descripcionError: String? = null,
    val precio: String = "",
    val precioError: String? = null,
    val categoriaId: Int? = null,
    val categoriaError: String? = null,
    val estadoProducto: String = "nuevo",
    val antiguedad: String? = null,
    val ubicacion: String? = null,
    val etiquetaIds: List<Int> = emptyList(),
    val availableCategories: List<com.renaix.domain.model.Category> = emptyList()
)
