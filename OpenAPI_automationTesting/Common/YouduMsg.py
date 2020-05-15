#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/3/27 16:04
# @Author  : hubiao
# @File    : YouduMsg.py

import requests

session = "{6CC14442-AB0E-409B-B56C-C8B98096A7EF}"

def setMsg(sendTo,title,conter):
    requests.post(f"http://192.168.2.203/zentao/www/index.php?m=api&f=setYouduMessBySession&session={session}&members={sendTo}&title={title}&cont={conter}")


sendTo = "胡彪_邵君兰"
title = "BV检查"
conter = "测试"

setMsg(sendTo,title,conter)