[app]
# Nome e pacotes
title = SportPredictor
package.name = sportpredictor
package.domain = org.sportpredictor
version = 1.0

# Pasta e extensões
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Requisitos para o Kivy e rede
requirements = python3,kivy,requests,certifi,urllib3,idna,chardet

# Configurações de Android
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.sdk_build_tools_version = 34.0.0
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# Estilo da App
orientation = portrait
fullscreen = 0
android.private_storage = True

[buildozer]
log_level = 2
warn_on_root = 1
