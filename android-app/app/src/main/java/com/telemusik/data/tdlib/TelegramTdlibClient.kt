package com.telemusik.data.tdlib

import org.drinkless.tdlib.Client
import org.drinkless.tdlib.TdApi

class TelegramTdlibClient(
    private val apiId: Int,
    private val apiHash: String,
) {
    private val client = Client.create({}, {}, {})

    fun requestAuthCode(phone: String) {
        client.send(TdApi.SetAuthenticationPhoneNumber(phone, null)) {}
    }

    fun submitAuthCode(code: String) {
        client.send(TdApi.CheckAuthenticationCode(code)) {}
    }

    fun loadChats(limit: Int = 100) {
        client.send(TdApi.GetChats(null, limit.toLong())) {}
    }

    fun loadChannelAudioHistory(chatId: Long, fromMessageId: Long = 0, limit: Int = 100) {
        client.send(
            TdApi.GetChatHistory(chatId, fromMessageId, 0, limit, false)
        ) {}
    }

    fun getFileDownloadUrl(fileId: Int, onReady: (String?) -> Unit) {
        client.send(TdApi.GetFile(fileId)) { obj ->
            val file = obj as? TdApi.File
            onReady(file?.local?.path)
        }
    }
}
