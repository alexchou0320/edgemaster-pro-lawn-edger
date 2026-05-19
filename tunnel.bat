@echo off
cd /d C:\site
"C:\Windows\System32\OpenSSH\ssh.exe" -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R 80:localhost:8080 nokey@localhost.run > C:\site\tunnel_url.txt 2>&1
