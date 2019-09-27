

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


def load(inputLanguage):
    if Language.Chinese == inputLanguage:
        pass
    elif Language.English == inputLanguage:
        pass
    else:
        raise ValueError('Language', inputLanguage)

    global Connect
    Connect = SpecificLoad(inputLanguage, [
        '連線',
        'Connect',
    ])
