@echo off
SETLOCAL
SET PROJECT_ROOT=%~dp0..

echo Activate virtual environment
echo:
call %PROJECT_ROOT%/venv/Scripts/activate.bat

echo Start getting words
pushd %PROJECT_ROOT%
python src/DictionaryCrawler.py
popd
echo Finished
echo:

echo Deactivate virtual environment
call %PROJECT_ROOT%/venv/Scripts/deactivate.bat


pause
