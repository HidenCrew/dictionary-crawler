REM there is Chinese in the path
chcp 65001

SETLOCAL
SET MY_PATH=%~dp0

for /r ".\" %%x in (*.mp3) do move "%%x" "%APPDATA%\Anki2\使用者 1\collection.media"

pause