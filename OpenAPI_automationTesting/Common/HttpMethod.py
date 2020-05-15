#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2018/7/31 17:18
# @Author  : hubiao
# @File    : HttpMethod.py
from Common.Config import ManageConfig
from Common import Log
import requests
import json

log = Log.MyLog()
class sendRequest:
    '''
    发送请求类
    '''
    def __init__(self,host,section,header=None):
        '''
        请求数据初始化
        @host：请求的地址前缀
        @header：请求头信息
        '''
        self.host = host
        self.header = header
        # 是否使用默认请求头
        if self.header is None:
            self.header = ManageConfig().getConfig('default')["json_header"]
        self.postSite = requests.session()
        self.section = section
        self.rf = ManageConfig().getConfig(self.section)
        self.wf = ManageConfig()

    def hooks(self,r,*args, **kwargs):
        '''
        为解决302跨域跳转到pds时，不传cookie实现的钩子方法，人为指定cookie并去请求302跳转连接
        :param r: 原始请求的响应信息
        :param args:
        :param kwargs:
        '''
        try:
            # 保存PDS和CASTGC Cookie，在PDS地址进行302跳转时使用
            if r.status_code == 200 and 'cookie' in r.request.headers.keys() and 'JSESSIONID' in r.request.headers['Cookie'] and 'CASTGC'in r.request.headers['Cookie'] and self.rf.get("pds") in r.request.url:
                self.wf.writeConfig(self.section, 'pdsCookie', r.request.headers['Cookie'])
            # 如果响应码是302，且location是PDS地址的跳转时，要加上PDS的cookie并请求这个location
            elif r.status_code == 302 and self.rf["pds"] in r.headers['location']:
                header = json.loads(self.header)
                header["cookie"] = self.rf["pdscookie"]
                self.postSite.request(method=r.request.method, url=r.headers['location'], headers=header,
                                      timeout=60)
        except BaseException as e:
            print("PDS 302异常开始分割线start: ".center(60, "#"))
            print("PDS 302跳转Url: " + r.request.url)
            print("PDS 302跳转出现异常: " + str(e))
            print("PDS 302异常结束分割线end: ".center(60, "#"))

    def JsonRequest(self,method,address,payload=None,header=None,website=None,funName =None):
        '''
        封装request方法，要求传三个参数
        @method：请求的方式post，get
        @address：请求的地址
        @payload：请求的body数据，可以不传，默认为空
        @return: 对响应信息进行重组，格式如下：
            {
                "status_code"：响应的http状态码
                "code": 响应体中的code，如果没有code将用status_code替代
                "msg": 响应的消息，当请求失败时，会返回对应的msg错误信息，服务器响应信息中没有这个字段时，不返回这个字段
                "data" 响应的具体数据（有些接口响应的是data，有些响应的是result，这里统一成data返回），服务器响应信息中没有这个字段时，不返回这个字段
                "success": 响应是否成功，服务器响应信息中没有这个字段时，不返回这个字段
            }
        '''
        try:
            # 如果website没有指定，组装请求地址
            if website is None:
                self.postUrl = ''.join([self.host,address])
            else:
                self.postUrl = address
            # 是否使用默认请求头
            if header is None:
                header = json.loads(self.header)
            # 判断payload不为str时，dumps成str类型
            if not isinstance(payload,str) and payload:
                payload = json.dumps(payload)
            # 发送POST请求
            self.Response = self.postSite.request(method=method,url=self.postUrl,data=payload,headers=header,hooks=dict(response=self.hooks),timeout=60)
            # 解决跨域302跳转后响应成cas登录页面的处理，当出现cas登录界面时自动重试相关接口
            if self.Response.status_code == 200 and "/login?service=" in self.Response.url:
                self.Response = self.postSite.request(method=method, url=self.postUrl, data=payload,
                                                      headers=json.loads(header),timeout=60)
            #打印请求和响应数据
            try:
                print("开始分割线start: ".center(60, "#"))
                if funName!=None: print("测试用例："+funName)
                print("请求方法: " + method)
                print("请求的Url: " + self.postUrl)
                print("持续时间: " + str(float('%.2f' % (self.Response.elapsed.total_seconds()*1000)))+' ms')
                print("请求数据: " + str(payload).encode('utf-8').decode("unicode_escape"))
                print("响应状态: " + str(self.Response.status_code))
                print("响应内容: " + self.Response.text)
                print("结束分割线end: ".center(60, "#"))
            except BaseException as e:
                print("打印请求和响应数据出现异常：" + str(e))
            res = {}
            res["status_code"] = self.Response.status_code
            # 当响应体为json类型，且响应信息不为空时
            if "application/json" in self.Response.headers["Content-Type"] and self.Response.text:
                Response = json.loads(self.Response.text)
                # 判断如果响应信息为dict时，重组逻辑
                if isinstance(Response, dict):
                    # 判断如果响应信息中有code和msg时对响应信息的重组处理，第二版本是code和data，第三版本是code和result
                    if 'code' in Response.keys() and 'msg' in Response.keys():
                        res["code"] = Response["code"]
                        res["msg"] = Response["msg"]
                        # 判断当响应信息有data时取data信息，有result取result，第二版本和第三版本响应的数据不在同一个对象里，其它情况报错
                        if 'data' in Response.keys():
                            res["data"] = Response["data"]
                        elif 'result' in Response.keys():
                            res["data"] = Response["result"]
                        else:
                            assert False
                        # 第三版本响应中多了success字段
                        if 'success' in Response.keys():
                            res["success"] = Response["success"]
                        # 第三版本响应中多了success字段
                        if 'loginToken' in Response.keys():
                            res["loginToken"] = Response["loginToken"]
                    # 第一版本接口出现异常时响应信息的处理
                    elif 'infoCode' in Response.keys():
                        res["code"] = self.Response.status_code
                        res["msg"] = Response["message"]
                    # 处理业务管理系统响应信息的处理
                    elif 'rtcode' in Response.keys():
                        res["code"] = Response["rtcode"]
                        res["msg"] = Response["rtmsg"]
                        if 'result' in Response.keys():
                            res["data"] = Response["result"]
                    else:
                        # 第一版本接口没有code和msg信息
                        res["code"] = self.Response.status_code
                        res["data"] = json.loads(self.Response.text)
                else:
                    # 非dict情况，直接把响应信息重组到data中，这是第一版本接口的响应，还有一些是直接响应的uuid的，都没有code、data、msg等信息
                    res["code"] = self.Response.status_code
                    res["data"] = json.loads(self.Response.text)
            else:
                #非json响应信息时的处理，直接把响应的文本重组给data
                res["code"] = self.Response.status_code
                res["data"] = self.Response.text
            return res
        except BaseException as e:
            print("异常开始分割线start: ".center(60, "#"))
            print("请求的Url: " + self.postUrl)
            print("请求数据: " + str(payload).encode('utf-8').decode("unicode_escape"))
            print("发送请求出现异常: " + str(e))
            print("异常结束分割线end: ".center(60, "#"))

if __name__ == '__main__':
    zentao = ManageConfig().getConfig('pds')
    print(type(zentao['header']))
    print(type(json.loads(zentao['header'])))
    print(zentao['pds'])
    print(zentao['header'])
    Response = sendRequest(zentao['pds'],zentao['header'])
    re = Response.JsonRequest("get","/rs/centerLogin/deployType")
    print(re)
    re = Response.JsonRequest("get","/rs/centerLogin/serverurl")
    print(re["data"])
    print(type(re))
    print(re)