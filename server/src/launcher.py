from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

from console import Console
from dynamic_data import DynamicData

url = 'https://github.com/PttCodingMan/uPtt/raw/develop/server/package/uPtt.zip'


console_obj = Console()
dynamic_data_obj = DynamicData(console_obj)

# resp = urlopen(url)
# zipfile = ZipFile(BytesIO(resp.read()))
# print(zipfile.namelist())