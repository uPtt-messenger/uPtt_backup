

class Language(object):

    Chinese = 1
    English = 2

    MinValue = Chinese
    MaxValue = English


LanguageList = [
    Language.Chinese,
    Language.English,
]


def SpecificLoad(inputLanguage, LangList):
    global LanguageList

    if len(LanguageList) != len(LangList):
        raise ValueError('SpecificLoad LangList legnth error')

    if inputLanguage not in LanguageList:
        raise ValueError('SpecificLoad Unknow language', inputLanguage)
    return LangList[LanguageList.index(inputLanguage)]


def replace(String, *args):
    for i in range(len(args)):
        Target = args[i]
        String = String.replace('{Target' + str(i) + '}', Target)
    return String


def load(inputLanguage):
    if Language.Chinese == inputLanguage:
        pass
    elif Language.English == inputLanguage:
        pass
    else:
        raise ValueError('Language', inputLanguage)

    global RecviveWaterballFrom
    RecviveWaterballFrom = SpecificLoad(inputLanguage, [
        '收到來自 {Target0} 的水球',
        'Recvive Waterball From {Target0}',
    ])

    global Re
    Re = SpecificLoad(inputLanguage, [
        '重新',
        'Re-',
    ])

    global Success
    Success = SpecificLoad(inputLanguage, [
        '成功',
        'Success',
    ])

    global Failed
    Failed = SpecificLoad(inputLanguage, [
        '失敗',
        'Failed',
    ])

    global LoginFail
    LoginFail = SpecificLoad(inputLanguage, [
        f'登入{Failed}',
        f'login {Failed}',
    ])

    global ReLoginFail
    ReLoginFail = SpecificLoad(inputLanguage, [
        f'{Re}登入{Failed}',
        f'{Re}login {Failed}',
    ])

    global LoginSuccess
    LoginSuccess = SpecificLoad(inputLanguage, [
        f'登入{Success}',
        f'login {Success}',
    ])

    global ReLoginSuccess
    ReLoginSuccess = SpecificLoad(inputLanguage, [
        f'{Re}登入{Success}',
        f'{Re}login {Success}',
    ])

    global NoSuchUser
    NoSuchUser = SpecificLoad(inputLanguage, [
        '無此使用者: {Target0}',
        'No Such User: {Target0}',
    ])

    global Welcome
    Welcome = SpecificLoad(inputLanguage, [
        '{Target0}! 歡迎您!',
        '{Target0}! Welcome!',
    ])

    global Logout
    Logout = SpecificLoad(inputLanguage, [
        '登出',
        'Logout',
    ])

    global LogoutSuccess
    LogoutSuccess = SpecificLoad(inputLanguage, [
        f'登出{Success}',
        f'Logout {Success}',
    ])

    global QueryUser
    QueryUser = SpecificLoad(inputLanguage, [
        '查詢使用者',
        'Query User',
    ])

    global UserOffline
    UserOffline = SpecificLoad(inputLanguage, [
        '使用者離線: {Target0}',
        'User Offline: {Target0}',
    ])

    global HaveNewMail
    HaveNewMail = SpecificLoad(inputLanguage, [
        '您有新信件',
        'You have new mail',
    ])

    global HaveNoMail
    HaveNoMail = SpecificLoad(inputLanguage, [
        '無新信件',
        'You have No mail',
    ])
