

import hashlib

# https://emn178.github.io/online-tools/sha256.html
def sha256(s):
    s_lower = s.lower()
    hash = hashlib.sha256(s_lower.encode('utf-8')).hexdigest()
    print(f'[{s}]\n[{s_lower}]\n[{hash}]')

# sha256('QQ_id')

# test
# import urllib.request, json
# with urllib.request.urlopen("https://raw.githubusercontent.com/PttCodingMan/uPtt_open_data/master/list/blacklist.json") as url:
#     data = json.loads(url.read().decode())
#     print(data)
