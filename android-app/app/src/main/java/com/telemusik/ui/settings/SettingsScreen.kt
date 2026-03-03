package com.telemusik.ui.settings

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun SettingsScreen() {
    var autoScrobble by remember { mutableStateOf(true) }
    var wifiOnlyDownloads by remember { mutableStateOf(true) }
    var cacheMb by remember { mutableIntStateOf(2048) }

    Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        Text("Settings")
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Text("Auto scrobble")
            Switch(checked = autoScrobble, onCheckedChange = { autoScrobble = it })
        }
        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Text("Downloads on Wi-Fi only")
            Switch(checked = wifiOnlyDownloads, onCheckedChange = { wifiOnlyDownloads = it })
        }
        Text("Offline cache limit: ${cacheMb} MB")
    }
}
