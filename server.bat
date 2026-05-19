@echo off
cd /d C:\site
"C:\Program Files\Python311\python.exe" -m http.server 8080 --directory C:\site
