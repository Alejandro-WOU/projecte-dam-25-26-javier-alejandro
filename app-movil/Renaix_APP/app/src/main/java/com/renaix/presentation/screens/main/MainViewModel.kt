package com.renaix.presentation.screens.main

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.renaix.domain.repository.AuthRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class MainViewModel(
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _selectedTab = MutableStateFlow(MainTab.Products)
    val selectedTab: StateFlow<MainTab> = _selectedTab.asStateFlow()

    private val _logoutState = MutableStateFlow<LogoutState>(LogoutState.Idle)
    val logoutState: StateFlow<LogoutState> = _logoutState.asStateFlow()

    /**
     * Cambia el tab seleccionado
     */
    fun selectTab(tab: MainTab) {
        _selectedTab.value = tab
    }

    fun logout() {
        viewModelScope.launch {
            _logoutState.value = LogoutState.Loading
            authRepository.logout()
            _logoutState.value = LogoutState.Success
        }
    }

    fun resetLogoutState() {
        _logoutState.value = LogoutState.Idle
    }
}

/**
 * Tabs disponibles en la navegación principal
 */
enum class MainTab {
    Products,
    Search,
    Map,
    Chat,
    Profile
}

/**
 * Estados del proceso de logout
 */
sealed class LogoutState {
    object Idle : LogoutState()
    object Loading : LogoutState()
    object Success : LogoutState()
}
