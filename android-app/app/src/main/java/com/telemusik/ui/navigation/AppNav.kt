package com.telemusik.ui.navigation

import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.telemusik.ui.channels.ChannelsScreen
import com.telemusik.ui.downloads.DownloadsScreen
import com.telemusik.ui.home.HomeScreen
import com.telemusik.ui.playlists.PlaylistsScreen
import com.telemusik.ui.profile.ProfileScreen

private val tabs = listOf("home", "channels", "playlists", "downloads", "profile")

@Composable
fun AppNav() {
    val nav = rememberNavController()
    val backStack by nav.currentBackStackEntryAsState()
    val route = backStack?.destination?.route

    Scaffold(
        bottomBar = {
            NavigationBar {
                tabs.forEach { tab ->
                    NavigationBarItem(
                        selected = route == tab,
                        onClick = { nav.navigate(tab) },
                        label = { Text(tab) },
                        icon = {},
                    )
                }
            }
        }
    ) { padding ->
        NavHost(navController = nav, startDestination = "home") {
            composable("home") { HomeScreen() }
            composable("channels") { ChannelsScreen() }
            composable("playlists") { PlaylistsScreen() }
            composable("downloads") { DownloadsScreen() }
            composable("profile") { ProfileScreen() }
        }
    }
}
