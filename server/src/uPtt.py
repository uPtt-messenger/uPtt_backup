from sys import argv
import os
import sys
from io import BytesIO
import zipfile
from urllib.request import urlopen
from urllib.error import HTTPError
from pathlib import Path

import log
from config import Config
from console import Console
from dynamic_data import DynamicData
from event import EventConsole
import util

LogPath = None


def log_to_file(msg):
    global LogPath
    if LogPath is None:
        desktop = os.path.join(
            os.path.join(
                os.environ['USERPROFILE']
            ),
            'Desktop'
        )

        LogPath = f'{desktop}/uPttLog.txt'

        print(LogPath)

    with open(LogPath, 'a', encoding='utf8') as f:
        f.write(f'{msg}\n')

config_obj = Config()

console_obj = Console()
console_obj.config = config_obj

if '-debug' in sys.argv or '-trace' in sys.argv:
    log.Handler = log_to_file
    config_obj.LogHandler = log_to_file

if '-trace' in sys.argv:
    config_obj.LogHandler = log.level.TRACE

if '-dev' in sys.argv:
    console_obj.run_mode = 'dev'

log.show_value(
    'uPtt',
    log.level.INFO,
    '執行模式',
    console_obj.run_mode
)

event_console = EventConsole()
console_obj.event = event_console

dynamic_data_obj = DynamicData(console_obj, run=False)

log.show_value(
    'uPtt',
    log.level.INFO,
    'Local version',
    config_obj.version)

log.show_value(
    'uPtt',
    log.level.INFO,
    'Dynamic version',
    dynamic_data_obj.data['version'])

version_local = config_obj.version
version_dynamic = dynamic_data_obj.data['version']

version_compare_result = util.compare_version(version_local, version_dynamic)
file_exist = Path(f'{config_obj.config_path}/uCore.exe').is_file()

if version_compare_result < 0 or not file_exist:

    if console_obj.run_mode == 'dev':
        url = 'https://github.com/PttCodingMan/uPtt/raw/develop/server/package/uCore.zip'
    else:
        url = 'https://github.com/PttCodingMan/uPtt/raw/master/server/package/uCore.zip'
    log.show(
        'uPtt',
        log.level.INFO,
        '開始更新')

    try:
        resp = urlopen(url)
    except HTTPError:
        log.show(
            'uPtt',
            log.level.INFO,
            '取得 uCore 檔案失敗')
        sys.exit()
    log.show(
        'uPtt',
        log.level.INFO,
        '更新完成')
    zip_file = zipfile.ZipFile(BytesIO(resp.read()))
    zip_file.extractall(path=config_obj.config_path)

a = ''
if len(argv) > 1:
    print(argv)
    a = ' ' + ' '.join(argv[1:])

    process = argv.copy()
    process[0] = f'{config_obj.config_path}/uCore.exe'
else:
    process = []
    process.append(f'{config_obj.config_path}/uCore.exe')

import subprocess

print(process)
subprocess.Popen(process)
