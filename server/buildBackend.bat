@echo off
cls

del /f uPtt.exe
del /f uLauncher.exe

rem nuitka --windows-disable-console --recurse-all src/uPtt.py

rem pyinstaller -w --onefile --icon="..\client\src\assets\images\uptt.ico" .\src\uPtt.py
rem pyinstaller -w --onefile .\src\uPtt.py
rem pyinstaller -w --onefile .\src\uLauncher.py
echo Build uPtt [Active]
nuitka --windows-disable-console --recurse-all src/uPtt.py
echo Build uPtt [Complete]

echo Sign uPtt [Active]
signtool sign /a /tr http://timestamp.comodoca.com uPtt.exe
echo Sign uPtt [Complete]

echo Sign uLauncher [Active]
nuitka --windows-disable-console --recurse-all src/uLauncher.py
echo Build uLauncher [Complete]
rem signtool sign /t http://timestamp.digicert.com /sha1 25eb809119b4052ebcbc106d163b6d5ff83116bb uLauncher.exe
rem signtool sign /tr http://timestamp.digicert.com /td sha256 /fd sha256 /as /sha1 25eb809119b4052ebcbc106d163b6d5ff83116bb uLauncher.exe
rem signtool sign /as /tr http://timestamp.comodoca.com /td sha256 /fd sha256 uLauncher.exe

echo Sign uLauncher [Active]
signtool sign /a /tr http://timestamp.comodoca.com uLauncher.exe
echo Sign uLauncher [Complete]

python zip.py

move uPtt.zip package
move uLauncher.zip package

:end
echo Finish