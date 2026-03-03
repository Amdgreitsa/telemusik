package com.telemusik.data.tdlib

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import org.drinkless.tdlib.Client
import org.drinkless.tdlib.TdApi

sealed interface TdAuthState {
    data object WaitingPhoneNumber : TdAuthState
    data object WaitingCode : TdAuthState
    data object WaitingPassword : TdAuthState
    data object Ready : TdAuthState
    data class Error(val message: String) : TdAuthState
}

data class TelegramAudioTrack(
    val messageId: Long,
    val chatId: Long,
    val fileId: Int,
    val title: String,
    val performer: String,
    val durationSec: Int,
)

class TelegramTdlibClient(
    private val apiId: Int,
    private val apiHash: String,
) {
    private val _authState = MutableStateFlow<TdAuthState>(TdAuthState.WaitingPhoneNumber)
    val authState: StateFlow<TdAuthState> = _authState

    private val client = Client.create(::onUpdate, ::onError, ::onFatalError)


    private fun onUpdate(update: TdApi.Object?) {
        when (update) {
            is TdApi.UpdateAuthorizationState -> when (update.authorizationState) {
                is TdApi.AuthorizationStateWaitPhoneNumber -> _authState.value = TdAuthState.WaitingPhoneNumber
                is TdApi.AuthorizationStateWaitCode -> _authState.value = TdAuthState.WaitingCode
                is TdApi.AuthorizationStateWaitPassword -> _authState.value = TdAuthState.WaitingPassword
                is TdApi.AuthorizationStateReady -> _authState.value = TdAuthState.Ready
                else -> Unit
            }
        }
    }

    private fun onError(error: Throwable?) {
        _authState.value = TdAuthState.Error(error?.message ?: "Unknown TDLib error")
    }

    private fun onFatalError(message: String?) {
        _authState.value = TdAuthState.Error(message ?: "Fatal TDLib error")
    }

    fun requestAuthCode(phone: String) {
        client.send(TdApi.SetAuthenticationPhoneNumber(phone, null)) { obj ->
            if (obj is TdApi.Error) _authState.value = TdAuthState.Error(obj.message)
        }
    }

    fun submitAuthCode(code: String) {
        client.send(TdApi.CheckAuthenticationCode(code)) { obj ->
            if (obj is TdApi.Error) _authState.value = TdAuthState.Error(obj.message)
        }
    }

    fun submitPassword(password: String) {
        client.send(TdApi.CheckAuthenticationPassword(password)) { obj ->
            if (obj is TdApi.Error) _authState.value = TdAuthState.Error(obj.message)
        }
    }

    fun loadPublicChannels(limit: Int = 100, onResult: (List<TdApi.Chat>) -> Unit) {
        client.send(TdApi.GetChats(TdApi.ChatListMain(), limit.toLong())) { response ->
            val chatIds = (response as? TdApi.Chats)?.chatIds ?: longArrayOf()
            val result = mutableListOf<TdApi.Chat>()
            if (chatIds.isEmpty()) {
                onResult(emptyList())
                return@send
            }
            var remaining = chatIds.size
            chatIds.forEach { id ->
                client.send(TdApi.GetChat(id)) { chatObj ->
                    val chat = chatObj as? TdApi.Chat
                    if (chat?.type is TdApi.ChatTypeSupergroup) {
                        result.add(chat)
                    }
                    remaining -= 1
                    if (remaining == 0) onResult(result)
                }
            }
        }
    }

    fun loadChannelAudioHistory(chatId: Long, fromMessageId: Long = 0, limit: Int = 100, onResult: (List<TelegramAudioTrack>) -> Unit) {
        client.send(TdApi.GetChatHistory(chatId, fromMessageId, 0, limit, false)) { obj ->
            val messages = (obj as? TdApi.Messages)?.messages ?: emptyArray()
            val audioTracks = messages.mapNotNull { message ->
                val audio = (message.content as? TdApi.MessageAudio)?.audio ?: return@mapNotNull null
                TelegramAudioTrack(
                    messageId = message.id,
                    chatId = chatId,
                    fileId = audio.audio.id,
                    title = audio.title ?: "Unknown",
                    performer = audio.performer ?: "Unknown",
                    durationSec = audio.duration,
                )
            }
            onResult(audioTracks)
        }
    }

    fun getFileDownloadPath(fileId: Int, onReady: (String?) -> Unit) {
        client.send(TdApi.DownloadFile(fileId, 1, 0, 0, true)) { obj ->
            val file = obj as? TdApi.File
            onReady(file?.local?.path)
        }
    }
}
