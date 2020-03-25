from io import BytesIO
import zipfile
from urllib.request import urlopen
from pathlib import Path

import log
from config import Config
from console import Console
from dynamic_data import DynamicData
from event import EventConsole
import util

config_obj = Config()

console_obj = Console()
console_obj.config = config_obj

event_console = EventConsole()
console_obj.event = event_console

dynamic_data_obj = DynamicData(console_obj, run=False)

log.show_value(
    'Launcher',
    log.level.INFO,
    'Local version',
    config_obj.version)

log.show_value(
    'Launcher',
    log.level.INFO,
    'Dynamic version',
    dynamic_data_obj.data['version'])

version_local = config_obj.version
version_dynamic = dynamic_data_obj.data['version']

version_compare_result = util.compare_version(version_local, version_dynamic)
file_exist = Path(f'{config_obj.config_path}/uPtt.exe').is_file()

if version_compare_result < 0 or not file_exist:
    url = 'https://github.com/PttCodingMan/uPtt/raw/develop/server/package/uPtt.zip'
    log.show(
        'Launcher',
        log.level.INFO,
        '開始更新')
    resp = urlopen(url)
    log.show(
        'Launcher',
        log.level.INFO,
        '更新完成')
    zip_file = zipfile.ZipFile(BytesIO(resp.read()))
    zip_file.extractall(path=config_obj.config_path)

# resp = urlopen(url)
# zipfile = ZipFile(BytesIO(resp.read()))
# print(zipfile.namelist())
