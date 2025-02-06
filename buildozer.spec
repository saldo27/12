[app]
title = TurnosApp
package.name = turnosapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
source.include_patterns = assets/*,images/*
source.exclude_dirs = tests, bin, .git
version = 1.0

requirements = python3,kivy,pillow,android

# Android specific settings
android.permissions = INTERNET
android.api = 34  # Updated for Android 14
android.minapi = 21
android.sdk = 34  # Updated for Android 14
android.ndk = 25b
android.accept_sdk_license = True
android.arch = arm64-v8a

# Orientation settings for Android 14
orientation = portrait
android.orientation = portrait
android.screenOrientation = portrait
android.manifest.orientation = portrait

# Add these lines for Android 14 compatibility
android.manifest.activity_config = orientation|screenSize
android.manifest.launch_mode = singleTop

# Bootstrap and dependencies
android.bootstrap = sdl2
android.enable_androidx = True

# Build settings
android.logcat_filters = *:S python:D
p4a.branch = master

# Gradle settings
android.gradle_dependencies = androidx.core:core:1.7.0, androidx.appcompat:appcompat:1.4.1

log_level = 2

[buildozer]
warn_on_root = 1
build_dir = ./.buildozer
bin_dir = ./bin
