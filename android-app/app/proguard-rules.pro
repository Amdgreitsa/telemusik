# Keep TDLib public API classes
-keep class org.drinkless.tdlib.** { *; }
-keep class org.drinkless.td.libcore.** { *; }

# Keep Room generated implementations
-keep class * extends androidx.room.RoomDatabase
-dontwarn org.jetbrains.annotations.**
