@echo off
cls

rmdir /s /q dist
rmdir /s /q PTTPostman.egg-info
cls
echo echo PTT Postman uploader v 1.0.0

python setup.py sdist
twine upload dist/*

echo Upload finish