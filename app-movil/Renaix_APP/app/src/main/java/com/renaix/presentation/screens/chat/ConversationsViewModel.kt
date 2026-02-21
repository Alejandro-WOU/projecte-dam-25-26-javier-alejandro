package com.renaix.presentation.screens.chat

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.renaix.domain.model.Conversation
import com.renaix.domain.repository.ChatRepository
import com.renaix.presentation.common.state.UiState
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class ConversationsViewModel(
    private val chatRepository: ChatRepository
) : ViewModel() {

    private val _conversations = MutableStateFlow<UiState<List<Conversation>>>(UiState.Idle)
    val conversations: StateFlow<UiState<List<Conversation>>> = _conversations.asStateFlow()

    init {
        loadConversations()
    }

    fun loadConversations() {
        viewModelScope.launch {
            _conversations.value = UiState.Loading
            chatRepository.getConversations()
                .onSuccess { conversations ->
                    _conversations.value = UiState.Success(conversations)
                }
                .onFailure { error ->
                    _conversations.value = UiState.Error(
                        error.message ?: "Error al cargar conversaciones"
                    )
                }
        }
    }

    fun refreshConversations() {
        loadConversations()
    }
}
