from util import sha256


def is_black_user(console_obj, ptt_id):
    current_hash_value = sha256(ptt_id)

    return current_hash_value in console_obj.dynamic_data.black_list
