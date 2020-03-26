@echo off
cls

cd dist
del /f uPtt.exe
cd ..

rem nuitka --windows-disable-console --recurse-all src/uPtt.py

rem pyinstaller -w --onefile --icon="..\client\src\assets\images\uptt.ico" .\src\uPtt.py
pyinstaller -w --onefile .\src\uPtt.py
rem pyinstaller -w --onefile .\src\uLauncher.py

IF EXIST "dist\uPtt.exe" (
  REM Do one thing
) ELSE (
    echo Build error
    goto end
)

cd dist
python zip.py
cd ..

copy dist\uPtt.zip package

:end
echo Finish