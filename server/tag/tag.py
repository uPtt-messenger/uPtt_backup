

import hashlib

def sha256(s):
    s_lower = s.lower()
    hash = hashlib.sha256(s_lower.encode('utf-8')).hexdigest()
    print(f'[{s}]\n[{s_lower}]\n[{hash}]')

sha256('QQ_id')