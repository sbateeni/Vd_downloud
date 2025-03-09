[app]
title = YT Downloader
package.name = ytdownloader
package.domain = org.yourname
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,kivymd,yt-dlp,requests

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1 