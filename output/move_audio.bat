SETLOCAL
SET MY_PATH=%~dp0

for /r ".\" %%x in (*.mp3) do move "%%x" "%APPDATA%\Anki2\User 1\collection.media"

pause
