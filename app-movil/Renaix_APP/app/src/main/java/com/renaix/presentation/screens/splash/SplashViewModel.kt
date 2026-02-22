package com.renaix.presentation.screens.splash

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.renaix.domain.repository.AuthRepository
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class SplashViewModel(
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _navigationEvent = MutableStateFlow<NavigationEvent>(NavigationEvent.None)
    val navigationEvent: StateFlow<NavigationEvent> = _navigationEvent.asStateFlow()

    init {
        checkSession()
    }

    private fun checkSession() {
        viewModelScope.launch {
            delay(2000)
            val hasValidSession = authRepository.hasValidSession()
            _navigationEvent.value = if (hasValidSession) {
                NavigationEvent.NavigateToMain
            } else {
                NavigationEvent.NavigateToLogin
            }
        }
    }

    fun onNavigationHandled() {
        _navigationEvent.value = NavigationEvent.None
    }
}

/**
 * Eventos de navegación desde el Splash
 */
sealed class NavigationEvent {
    object None : NavigationEvent()
    object NavigateToLogin : NavigationEvent()
    object NavigateToMain : NavigationEvent()
}
