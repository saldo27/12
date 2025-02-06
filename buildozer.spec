[app]
title = TurnosApp
package.name = turnosapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
source.include_patterns = assets/*,images/*
source.exclude_dirs = tests, bin, .git
version = 1.0

requirements = python3,kivy,pillow

# Android specific settings
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.accept_sdk_license = True
android.arch = arm64-v8a

# Orientation settings
orientation = portrait
android.orientation = portrait

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
