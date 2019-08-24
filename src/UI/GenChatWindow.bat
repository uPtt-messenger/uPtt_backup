@echo off
cls

@echo hi
..\..\venv\Scripts\pyuic5.exe -x chatwindow.ui -o ..\main\python\ChatWindow.py
