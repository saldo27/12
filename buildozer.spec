[app]
title = TurnosApp
package.name = turnosapp
package.domain = org.turnosapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.2.1
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.private_storage = True
android.entrypoint = org.kivy.android.PythonActivity
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
