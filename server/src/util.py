import hashlib


def sha256(ptt_id):
    s_lower = ptt_id.lower()
    hash_value = hashlib.sha256(s_lower.encode('utf-8')).hexdigest()
    # print(f'[{ptt_id}]\n[{s_lower}]\n[{hash_value}]')
    return hash_value
