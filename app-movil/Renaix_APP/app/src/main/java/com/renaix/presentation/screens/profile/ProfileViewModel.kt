package com.renaix.presentation.screens.profile

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.renaix.domain.model.User
import com.renaix.domain.repository.AuthRepository
import com.renaix.domain.repository.UserRepository
import com.renaix.presentation.common.state.UiState
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class ProfileViewModel(
    private val userRepository: UserRepository,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _state = MutableStateFlow<UiState<User>>(UiState.Loading)
    val state: StateFlow<UiState<User>> = _state.asStateFlow()

    private val _logoutState = MutableStateFlow<UiState<Unit>>(UiState.Idle)
    val logoutState: StateFlow<UiState<Unit>> = _logoutState.asStateFlow()

    init {
        loadProfile()
    }

    fun loadProfile() {
        viewModelScope.launch {
            _state.value = UiState.Loading

            userRepository.getProfile()
                .onSuccess { user ->
                    _state.value = UiState.Success(user)
                }
                .onFailure { exception ->
                    _state.value = UiState.Error(exception.message ?: "Error al cargar perfil")
                }
        }
    }

    fun logout() {
        viewModelScope.launch {
            _logoutState.value = UiState.Loading
            authRepository.logout()
            _logoutState.value = UiState.Success(Unit)
        }
    }
}
