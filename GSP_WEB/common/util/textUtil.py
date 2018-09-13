#-*- coding: utf-8 -*-
def NullStringToNull(_string):
    if _string == "":
        return None
    else:
        return _string

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# 문자열에서 숫자를 제외한 나머지 문자를 지운다
def remove_char_except_digit(str_src):
    return ''.join([c for c in str_src if c.isdigit()])
