import os
import sys
from time import gmtime, strftime

# Log Handler
Handler = None


class Level(object):

    TRACE = 1
    DEBUG = 2
    INFO = 3
    SLIENT = 4

    MinValue = TRACE
    MaxValue = SLIENT


LogLevel = Level.INFO


def merge(Msg) -> str:
    if isinstance(Msg, list):
        for i in range(len(Msg)):
            if len(Msg[i]) == 0:
                continue
            if Msg[i][0].upper() != Msg[i][0].lower() and i != 0:
                Msg[i] = ' ' + Msg[i].lstrip()
            if (Msg[i][-1].upper() != Msg[i][-1].lower() and
                    i != len(Msg) - 1):
                Msg[i] = Msg[i].rstrip() + ' '

        Msg = ''.join(Msg)
    Msg = str(Msg)
    Msg = Msg.replace('  ', ' ')

    return Msg


def show(PreFix, CurrentLogLevel, Msg):

    global LogLevel

    if LogLevel > CurrentLogLevel:
        return
    if len(Msg) == 0:
        return

    Msg = merge(Msg)

    TotalMessage = '[' + strftime('%m%d %H%M%S') + ']'

    if CurrentLogLevel == Level.DEBUG:
        TotalMessage += '[除錯]'
    elif CurrentLogLevel == Level.INFO:
        TotalMessage += '[資訊]'

    if PreFix is not None:
        TotalMessage += '[' + PreFix + ']'
    TotalMessage += ' ' + Msg

    try:
        print(TotalMessage.encode(
            sys.stdin.encoding,
            'replace'
        ).decode(
            sys.stdin.encoding
        ))
    except Exception:
        print(TotalMessage.encode('utf-8', "replace").decode('utf-8'))

    global Handler
    if Handler is not None:
        Handler(TotalMessage)


LastValue = None


def showvalue(PreFix, CurrentLogLevel, Msg, Value):

    global LogLevel
    if LogLevel > CurrentLogLevel:
        return
    global LastValue

    if isinstance(Value, list):
        Value = Value.copy()

    Msg = merge(Msg)

    Value = merge(Value)
    if len(Msg) == 0:
        return
    # if len(Value) == 0:
    #     return

    TotalMessage = []
    TotalMessage.append(Msg)
    TotalMessage.append(' [')
    TotalMessage.append(Value)
    TotalMessage.append(']')

    show(PreFix, LogLevel, ''.join(TotalMessage))

    LastValue = Value

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
