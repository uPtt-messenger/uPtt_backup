import sys
from time import gmtime, strftime

# Log Handler
Handler = None


class level(object):
    TRACE = 1
    DEBUG = 2
    INFO = 3
    SILENT = 4

    MinValue = TRACE
    MaxValue = SILENT


Log_level = level.INFO


def merge(msg) -> str:
    if isinstance(msg, list):
        for i in range(len(msg)):
            if len(msg[i]) == 0:
                continue
            if msg[i][0].upper() != msg[i][0].lower() and i != 0:
                msg[i] = ' ' + msg[i].lstrip()
            if (msg[i][-1].upper() != msg[i][-1].lower() and
                    i != len(msg) - 1):
                msg[i] = msg[i].rstrip() + ' '

        msg = ''.join(msg)
    msg = str(msg)
    msg = msg.replace('  ', ' ')

    return msg


def show(prefix, current_log_level, msg):
    global Log_level

    if Log_level > current_log_level:
        return
    if len(msg) == 0:
        return

    msg = merge(msg)

    total_message = '[' + strftime('%m%d %H%M%S') + ']'

    if current_log_level == level.DEBUG:
        total_message += '[除錯]'
    elif current_log_level == level.INFO:
        total_message += '[資訊]'

    if prefix is not None:
        total_message += '[' + prefix + ']'
    total_message += ' ' + msg

    try:
        print(total_message.encode(
            sys.stdin.encoding,
            'replace'
        ).decode(
            sys.stdin.encoding
        ))
    except Exception:
        print(total_message.encode('utf-8', "replace").decode('utf-8'))

    global Handler
    if Handler is not None:
        Handler(total_message)


LastValue = None


def show_value(prefix, current_log_level, msg, value):
    global Log_level
    if Log_level > current_log_level:
        return
    global LastValue

    if isinstance(value, list):
        value = value.copy()

    msg = merge(msg)

    value = merge(value)
    if len(msg) == 0:
        return
    # if len(Value) == 0:
    #     return

    total_message = []
    total_message.append(msg)
    total_message.append(' [')
    total_message.append(value)
    total_message.append(']')

    show(prefix, Log_level, ''.join(total_message))

    LastValue = value

#                        ____________
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#  _____________________|            |_____________________
# |                                                        |
# |                                                        |
# |                                                        |
# |_____________________              _____________________|
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |____________|


# 耶和華是我的牧者，我必不致缺乏。
# 他使我躺臥在青草地上，領我在可安歇的水邊。
# 他使我的靈魂甦醒，為自己的名引導我走義路。
# 我雖然行過死蔭的幽谷，也不怕遭害，因為你與我同在；你的杖，你的竿，都安慰我。
# 在我敵人面前，你為我擺設筵席；你用油膏了我的頭，使我的福杯滿溢。
# 我一生一世必有恩惠慈愛隨著我；我且要住在耶和華的殿中，直到永遠。
# - 詩篇 23篇
