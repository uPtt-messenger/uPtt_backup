@echo off
cls

del /f uPtt.exe
del /f uLauncher.exe

python -m nuitka --standalone --windows-dependency-tool=pefile --experimental=use_pefile_recurse --experimental=use_pefile_fullrecurse src/uPtt.py

rem echo Sign uLauncher [Active]
rem signtool sign /a /tr http://timestamp.comodoca.com uLauncher.exe
rem echo Sign uLauncher [Complete]

rem python zip.py

rem move uPtt.zip package
rem move uLauncher.zip package

:end
echo Finish