@echo off
cls

del /f uPtt.exe

rem nuitka --windows-disable-console --recurse-all src/uPtt.py

rem pyinstaller -w --onefile --icon="..\client\src\assets\images\uptt.ico" .\src\uPtt.py
rem pyinstaller -w --onefile .\src\uPtt.py
rem pyinstaller -w --onefile .\src\uLauncher.py
nuitka --windows-disable-console --recurse-all src/uPtt.py

IF EXIST "uPtt.exe" (
  REM Do one thing
) ELSE (
    echo Build error
    goto end
)

nuitka --windows-disable-console --recurse-all src/uLauncher.py

IF EXIST "uLauncher.exe" (
  REM Do one thing
) ELSE (
    echo Build error
    goto end
)


cd dist
python zip.py
cd ..

move uPtt.zip package
move uLauncher.zip package

:end
echo Finish