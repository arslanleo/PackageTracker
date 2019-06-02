@echo off

start cmd.exe /k "cd /d env\Scripts\ & activate & cd /d ..\.. & python manage.py runserver"
start C:\"Program Files (x86)"\Google\Chrome\Application\chrome.exe "http://127.0.0.1:8000/"