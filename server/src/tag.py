import hashlib


def sha256(ptt_id):
    s_lower = ptt_id.lower()
    hash_value = hashlib.sha256(s_lower.encode('utf-8')).hexdigest()
    # print(f'[{ptt_id}]\n[{s_lower}]\n[{hash_value}]')
    return hash_value


class Tag:
    def __init__(self, console_obj):
        self.console = console_obj

    def get_tag(self, ptt_id):
        current_hash_value = sha256(ptt_id)

        if current_hash_value in self.console.dynamic_data.tag_data:
            return self.console.dynamic_data.tag_data[current_hash_value]
        return None
