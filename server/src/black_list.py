from util import sha256


def is_black_user(dynamic_data, ptt_id):
    current_hash_value = sha256(ptt_id)

    return current_hash_value in dynamic_data.black_list
