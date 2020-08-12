@echo off
cls

echo Sign %1 [Active]
signtool sign /a /tr http://timestamp.comodoca.com %1.exe
echo Sign %1 [Complete]

python zip.py %1.exe

move %1.zip package

echo Finish