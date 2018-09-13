#-*- coding: utf-8 -*-
from datetime import datetime
import time

# '20001231' 스트링 형식의 날짜를 datetime 오브젝트로 변환
from dateutil import parser, tz

from GSP_WEB.common.util.textUtil import remove_char_except_digit


# '2000-12-31', '2000/12/31' 등등의 날짜 문자열을 datetime 오브젝트로 변환
def string_to_date(yyyymmdd):

    # yyyymmdd 는 문자열 타입일것
    if not isinstance(yyyymmdd, str):
        return None

    yyyymmdd = remove_char_except_digit(yyyymmdd)

    if len(yyyymmdd) != 8:
        return None

    yyyy = int(yyyymmdd[:4])
    mm = int(yyyymmdd[4:6])
    dd = int(yyyymmdd[6:])
    return datetime(yyyy, mm, dd)


# '2000-01-01' 스트링 형식의 날짜를 입력받아 현재 시간과의 날짜 차이를 계산
def date_delta(yyyymmdd):

    # yyyymmdd 는 문자열 타입일것
    if not isinstance(yyyymmdd, str):
        return None

    d = string_to_date(yyyymmdd)
    return (datetime.date.today() - d).days

def Local2UTC(LocalTime):
    EpochSecond = time.mktime(LocalTime.timetuple())
    utcTime = datetime.utcfromtimestamp(EpochSecond)

    return utcTime

def UTC2Local(sourceTime):
    utcTime = parser.parse(sourceTime)
    epoch = time.mktime(utcTime.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    result = utcTime + offset
    return result.strftime('%Y-%m-%d %H:%M:%S')
    #from_zone = tz.tzutc()
    #strDate = parser.parse(utcTime).strftime('%Y-%m-%d %H:%M:%S')

