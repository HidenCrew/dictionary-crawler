REM there is Chinese in the path
chcp 65001

SETLOCAL
SET PROJECT_ROOT=%~dp0..

pushd %PROJECT_ROOT%\output
for /r ".\" %%x in (*.mp3) do move "%%x" "%APPDATA%\Anki2\使用者 1\collection.media"
popd

pause