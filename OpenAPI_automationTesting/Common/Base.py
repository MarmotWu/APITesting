#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by hubiao on 2017/5/9
from __future__ import print_function
import os,requests
import hashlib
import base64
import time
import calendar
import subprocess
from functools import wraps
from datetime import datetime
from datetime import timedelta

def upFiles(address,fileName):
    '''
    封装上传文件方法，要求传二个参数，上传成功返回文件UUID
    @address：请求的地址
    @fileName：要上传的文件，相对于工程目录
    '''
    if not os.path.exists(fileName):
        return None
    try:
        re = requests.request('post',address,files={'file':open(fileName,'rb')})
        #发送POST请求
        return re.text
    except Exception as e:
        print(e)
        return None

def getFileMD5(fileName):
    '''
    传入一个文件，输出文件MD5
    @fileName：要获取MD5值的文件名称，相对于工程目录
    '''
    if not os.path.exists(fileName):
        return None
    try:
        fileObjct = open(fileName, 'rb')
        m = hashlib.md5()
        while True:
            d = fileObjct.read(4096) #每次读取4KB的数据
            if not d: break #如果读出来的数据为空时跳出循环
            m.update(d)
        fileObjct.close()
        return m.hexdigest()
    except Exception as e:
        print(e)
        return None

def getStrMD5(String):
    '''
    传入一个字符串，返回字符串MD5值
    :param String: 字符串
    :return:MD5值
    '''
    m = hashlib.md5()
    m.update(String.encode('utf-8'))
    return m.hexdigest()

def getStrSha1(msg):
    """
    sha1 算法加密
    :param msg: 需加密的字符串
    :return: 加密后的字符
    """
    sh = hashlib.sha1()
    sh.update(msg.encode('utf-8'))
    return sh.hexdigest()

def ToBase64(String):
    '''
    传入一个字符串，返回字符串MD5值
    :param String: 字符串
    :return:MD5值
    '''
    base64Str = base64.b64encode(String.encode("utf-8"))
    return str(base64Str,'utf-8')

def FromBase64(String):
    '''
    传入一个字符串，返回字符串MD5值
    :param String: 字符串
    :return:MD5值
    '''
    original = base64.b64decode(String)
    return str(original,'utf-8')

def getUnix(date=None):
    '''
    通过传入的时间获取时间戳，默认获取当前时间戳
    :param date:传入的时间，格式为：'2017-05-09 18:31:22' 
    :return: 返回时间戳
    '''
    if date is None:
        ST = datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),"%Y-%m-%d %H:%M:%S")
    else:
        ST = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    unixST = int(time.mktime(ST.timetuple())) * 1000
    return str(unixST)

def UnixToTime(unix):
    '''
    把时间戳转换成时间
    :param unix: 时间戳
    :return: 返回时间
    '''
    time_local = time.localtime(int(unix)/1000)
    dt = time.strptime(time.strftime("%Y-%m-%d %H:%M:%S",time_local),"%Y-%m-%d %H:%M:%S")
    return dt

def getRecentMonthOfDay():
    '''
    获取近一个月的开始时间,比如今天是2016-12-15 12:25:00，那么返回的时间为2016-11-15 00:00:00
    :return: 返回最近一个月的开始时间
    '''
    d = datetime.strptime(time.strftime('%Y-%m-%d',time.localtime(time.time())),"%Y-%m-%d")
    year = d.year
    month = d.month

    if month == 1 :
        month = 12
        year -= 1
    else :
        month -= 1
    days = calendar.monthrange(year, month)[1]
    #上月同一天00:00到当前这一刻，认定为最近一月，如果要为上一天数据days减1即可
    day = d- timedelta(days=days)
    unixtime = int(time.mktime(day.timetuple()))*1000
    return unixtime,day

def calday(month, year):
    '''
    根据指定的年月，返回当月天数
    :param month: 月份
    :param year: 年份
    :return: 返回指定年月当月天数
    '''
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        days = "31"
        return days
    elif month == 4 or month == 6 or month == 9 or month == 11:
        days = "30"
        return days
    elif month == 2:
        if calendar.isleap(year):
            days = "29"
            return days
        else:
            days = "28"
            return days

def shell(cmd):
    output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    o = output.decode("utf-8")
    return o

if __name__ == "__main__":
    md = getFileMD5("Base.py")
    print(ToBase64('hubiao'))
    print(FromBase64('aHViaWFv'))
    print(md)