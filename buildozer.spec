[app]
# Title of your application
title = TurnosApp

# Package name
package.name = turnosapp

# Name of your main Python file
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Main Python module (the one containing your main.py)
source.include_patterns = assets/*,images/*

# Version of your app
version = 1.0

# Requirements
requirements = python3,kivy

# Android specific
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 23b
android.accept_sdk_license = True

# Architecture
android.arch = arm64-v8a

[buildozer]
# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Path to build directory (default: ./.buildozer)
build_dir = ./.buildozer

# Path to build artifact storage (default: ./bin)
bin_dir = ./bin

# Whether to clear build directory before each build
warning.disable = 0
