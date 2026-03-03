package com.telemusik.ui.login

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun LoginScreen(onLogin: (String, String) -> Unit = { _, _ -> }) {
    val (phone, setPhone) = remember { mutableStateOf("") }
    val (code, setCode) = remember { mutableStateOf("") }

    Column(
        verticalArrangement = Arrangement.spacedBy(12.dp),
        modifier = Modifier.padding(16.dp)
    ) {
        Text("Telegram Login")
        OutlinedTextField(
            value = phone,
            onValueChange = setPhone,
            label = { Text("Phone") },
            modifier = Modifier.fillMaxWidth(),
        )
        OutlinedTextField(
            value = code,
            onValueChange = setCode,
            label = { Text("Code") },
            modifier = Modifier.fillMaxWidth(),
        )
        Button(onClick = { onLogin(phone, code) }, modifier = Modifier.fillMaxWidth()) {
            Text("Authorize")
        }
    }
}
