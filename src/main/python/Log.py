import sys
from time import gmtime, strftime

import Config
import Util

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


def log(PreFix, CurrentLogLevel, Msg):

    if not Util.checkRange(Level, CurrentLogLevel):
        raise ValueError('LogLevel', CurrentLogLevel)

    global LogLevel

    if LogLevel > CurrentLogLevel:
        return
    if len(Msg) == 0:
        return
    Msg = merge(Msg)

    TotalMessage = '[' + strftime('%m%d %H:%M:%S') + ']'

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


def showValue(PreFix, CurrentLogLevel, Msg, Value):

    if not Util.checkRange(Level, CurrentLogLevel):
        raise ValueError('LogLevel', CurrentLogLevel)

    global LogLevel
    if LogLevel > CurrentLogLevel:
        return
    global LastValue

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

    log(PreFix, LogLevel, ''.join(TotalMessage))

    LastValue = Value
