#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/1/2 11:19
# @Author  : hubiao
# @File    : PublicLogin.py
from Common.Config import ManageConfig
from Common import HttpMethod
from Common import Base
import json,re,sys

class BimAdmin:
    '''
    BimAdmin 登录类
    '''
    def __init__(self,section = 'sysadmin'):
        self.section = section
        self.rf = ManageConfig().getConfig(self.section)
        self.header = ManageConfig().getConfig('default')["urlencoded_header"]
        self.body = self.rf["logininfo"]
        self.BimAdminLogin = HttpMethod.sendRequest(self.rf['host'],section=self.section)

    def Login(self):
        '''
        后台登录
        :param BimAadminLogin:
        :return:
        '''
        resource = "/login.htm"
        response = self.BimAdminLogin.JsonRequest("post",resource,self.body,self.header)
        assert response["status_code"] == 200
        return self.BimAdminLogin

class Center:
    '''
    Center CAS登录类
    '''
    def __init__(self,centerusername,centerpassword,section='center'):
        self.section = section
        self.rf = ManageConfig().getConfig(self.section)
        self.wf = ManageConfig()
        self.productId = self.rf['centerProductId']
        self.username = centerusername
        self.password = centerpassword
        self.header = ManageConfig().getConfig('default')["plain_header"]
        self.CenterLogin = HttpMethod.sendRequest(self.rf['pds'],section=self.section)
        self.epid = ''

    def getServerUrl(self):
        '''
        获取服务器地址信息
        '''
        resource = '/rs/centerLogin/serverurl'
        response = self.CenterLogin.JsonRequest('get',resource)
        serverlist = response["data"]
        assert response["status_code"] == 200
        assert len(serverlist) != 0
        for server in serverlist:
            self.wf.writeConfig(self.section,server["serverName"],server["serverURL"])

    def getDeployType(self):
        '''
        获取部署类型
        :return:
        '''
        resource = '/rs/centerLogin/deployType'
        response = self.CenterLogin.JsonRequest('get', resource)
        assert response["status_code"] == 200
        deployType = response["data"]
        self.wf.writeConfig(self.section,'deployType', deployType)

    def getLT(self):
        '''
        获取LT
        :return:
        '''
        resource = '/login'
        response = self.CenterLogin.JsonRequest('get', resource)
        assert response["status_code"] == 200
        html = response["data"]
        pattern = 'value="LT(.+?)" />'
        lt = re.findall(pattern, html)[0]
        return lt

    def getTGC(self):
        '''
        获取TGC，依赖getLT接口
        :return:
        '''
        resource = '/login'#?service=+serverlist[6]["serverURL"].replace("://","%3A%2F%2F")
        body = r'_eventId=submit&execution=e1s1&lt=LT{self.getLT()}&password={self.password}&productId={self.productId}&submit=%25E7%2599%25BB%25E5%25BD%2595&username={self.username}'
        response = self.CenterLogin.JsonRequest('post',resource,body,self.header)
        assert response["status_code"] == 200

    def getCompanyList(self):
        '''
        获取企业id列表
        :return:
        '''
        resource = "/rs/centerLogin/companyList"
        body = {"password": self.password,"username": self.username}
        response = self.CenterLogin.JsonRequest('post',resource,body)
        assert response["status_code"] == 200
        response = response["data"]
        if len(response) > 0:
            self.wf.writeConfig(self.section,'epid',response[0]["epid"])
            self.epid = response[0]["epid"]
            return response[0]["epid"]

    def switchCompany(self):
        '''
        切换到指定企业，依赖getCompanyList接口
        :return:
        '''
        resource = "/rs/centerLogin/login"
        body = {"epid":self.epid,"password": self.password,"username": self.username}
        response = self.CenterLogin.JsonRequest('post',resource,body)
        assert response["status_code"] == 200

    def Login(self):
        '''
        Center登录
        :return:
        '''
        self.getServerUrl()
        self.getDeployType()
        self.getTGC()
        self.getCompanyList()
        self.switchCompany()

class BV:
    '''
    BV CAS登录类
    '''
    def __init__(self,username,password,section = 'mylubanapp'):
        self.section = section
        self.rf = ManageConfig().getConfig(self.section)
        self.wf = ManageConfig()
        self.productId = self.rf['BVproductId']
        self.username = username
        self.password = password
        self.header = ManageConfig().getConfig('default')["plain_header"]
        self.casLogin = HttpMethod.sendRequest(self.rf['pds'],section=self.section)
        self.epid = ''

    def getServerUrl(self):
        '''
        获取服务器地址信息
        '''
        resource = '/rs/casLogin/serverUrl'
        response = self.casLogin.JsonRequest('get',resource)
        serverlist = response["data"]
        assert response["status_code"] == 200
        assert len(serverlist) != 0
        for server in serverlist:
            self.wf.writeConfig(self.section,server["serverName"],server["serverURL"])

    def getLT(self):
        '''
        获取LT
        :return:
        '''
        resource = '/login'
        response = self.casLogin.JsonRequest('get', resource)
        assert response["status_code"] == 200
        html = response["data"]
        pattern = 'value="LT(.+?)" />'
        lt = re.findall(pattern, html)[0]
        return lt

    def getTGC(self):
        '''
        获取TGC，依赖getLT接口
        :return:
        '''
        resource = '/login'#?service=+serverlist[6]["serverURL"].replace("://","%3A%2F%2F")
        body = r'_eventId=submit&execution=e1s1&lt=LT{self.getLT()}&password={self.password}&productId={self.productId}&submit=%25E7%2599%25BB%25E5%25BD%2595&username={self.username}'
        response = self.casLogin.JsonRequest('post',resource,body,self.header)
        assert response["status_code"] == 200

    def getCompanyList(self):
        '''
        获取企业id列表
        :return:
        '''
        resource = "/rs/casLogin/companyList"
        body = {"password": self.password,"userName": self.username, "clientVersion": "5.8.0",
         "phoneModel": "国行(A1865)、日行(A1902)iPhone X", "platform": "ios", "innetIp": "192.168.7.184", "productId": self.productId,
         "token": "f54d6c8c13445a723a2863a72d460e5aec48010560ea2351bda6474de5164899", "systemVersion": "12.1.2",
         "hardwareCodes": "3465192946d57f13482640578c77ffa77d1f66a4"}
        response = self.casLogin.JsonRequest('post',resource,body)
        assert response["status_code"] == 200
        response = response["data"]
        if len(response) > 0:
            self.wf.writeConfig(self.section,'epid',response[0]["enterpriseId"])
            self.epid = response[0]["enterpriseId"]
            return self.epid

    def switchCompany(self):
        '''
        切换到指定企业
        :return:
        '''
        resource = r"/rs/casLogin/changeEnterprise/{self.epid}"
        response = self.casLogin.JsonRequest('get',resource)
        assert response["status_code"] == 200

    def Login(self):
        '''
        登录BV CAS流程方法
        :return:
        '''
        self.getServerUrl()
        self.getTGC()
        self.getCompanyList()
        self.switchCompany()

class OpenAPI():
    '''
    开放平台登录类
    '''
    def __init__(self,apikey,apisecret,section='openapi'):
        self.section = section
        self.rf = ManageConfig().getConfig(self.section)
        self.wf = ManageConfig()
        self.apikey = 'd46e1fcf4c07ce4a69ee07e4134bcef1'
        self.apisecret = '6659d4d1cdba61ceb1db9942a4a74f41'
        self.username = 'sunli'
        self.OpenAPIToken = HttpMethod.sendRequest(self.rf['openapiurl'],section=self.section)

    def Login(self):
        '''
        登录获取token
        '''
        resource = r"/rs/token/"+self.apikey+"/"+self.apisecret+"/"+self.username
        #resource = r"/rs/token/"+self.apikey+"/"+self.apisecret
        response = self.OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        # 获取到响应的token并更新到header中
        header = json.loads(self.OpenAPIToken.header)
        token = {"token": response["data"]}
        header.update(token)
        self.OpenAPIToken.header = json.dumps(header)
        return self.OpenAPIToken

class Bimapp:
    '''
    Bimapp 登录类
    '''
    def __init__(self,username,password,section='bimapp'):
        self.section = section
        self.rf = ManageConfig().getConfig(self.section)
        self.wf = ManageConfig()
        self.username = Base.ToBase64(username)
        self.password = password
        self.token = ''
        self.AcAddress = ''
        self.BimappLogin = HttpMethod.sendRequest(self.rf['host'],section=self.section)

    def GetCookie(self):
        '''
        获取cookie
        '''
        resource = "/login.htm"
        response = self.BimappLogin.JsonRequest('get', resource)
        assert response["status_code"] == 200

    def GetAcAddress(self):
        '''
        获取ac地址
        '''
        resource = "/getAcAddress.htm"
        response = self.BimappLogin.JsonRequest('get', resource)
        assert response["status_code"] == 200
        if response.get('data') or response.get('data') is not None:
            self.wf.writeConfig(self.section, 'AcAddress', response.get('data'))
            self.AcAddress = response.get('data')

    def Gettoken(self):
        '''
        获取token
        '''
        resource = r"{self.AcAddress}/rs/rest/user/login/{self.username}/{self.password}"
        response = self.BimappLogin.JsonRequest('get', resource,website=self.AcAddress)
        assert response["status_code"] == 200
        self.token = response.get('loginToken')

    def DoLoginWithToken(self):
        '''
         token登录
        '''
        resource = r"/bimapp/doLoginWithToken.htm?token={self.token}"
        response = self.BimappLogin.JsonRequest('get', resource)
        assert response["status_code"] == 200


    def Login(self):
        '''
        登录
        '''
        self.GetCookie()
        self.GetAcAddress()
        self.Gettoken()
        self.DoLoginWithToken()
        return self.BimappLogin


class MylubanWeb:
    '''
    MylubanWeb 登录类
    '''
    def __init__(self,username,password,section='MylubanWeb'):
        self.section = section
        self.rf = ManageConfig().getConfig(self.section)
        self.username = username
        self.password = password
        self.MylubanWebLogin = HttpMethod.sendRequest(self.rf['host'],section=self.section)

    def Login(self):
        '''
        MylubanWeb登录
        :param MylubanWebLogin:
        :return:
        '''
        resource = "/myluban/rest/login"
        body = {"username":self.username,"password":self.password}
        response = self.MylubanWebLogin.JsonRequest('post',resource,body)
        assert response["status_code"] == 200
        return self.MylubanWebLogin

class Bussiness:
    '''
    Bussiness 登录类
    '''
    def __init__(self,username,password,section = 'Bussiness'):
        self.section = section
        self.rf = ManageConfig().getConfig(self.section)
        self.username = username
        self.password = password
        self.BussinessLogin = HttpMethod.sendRequest(self.rf['host'],section=self.section)

    def Login(self):
        '''
        Bussiness 登录
        :param BussinessLogin:
        :return:
        '''
        resource = "/login"
        body = {"username":self.username,"password":self.password}
        response = self.BussinessLogin.JsonRequest('post',resource,body)
        assert response["status_code"] == 200
        return self.BussinessLogin

class lubansoft:
    '''
    lubansoft 登录类
    '''
    def __init__(self,username,password,section = 'lubansoft'):
        self.section = section
        self.rf = ManageConfig().getConfig(self.section)
        self.username = username
        self.password = password
        self.header = ManageConfig().getConfig('default')["soap_header"]
        self.lubansoftLogin = HttpMethod.sendRequest(self.rf['host'],section=self.section,header=self.header)

    def Login(self):
        '''
        lubansoft 登录
        :return:
        '''
        resource = "/login"
        body = '''<?xml version="1.0" encoding="UTF-8"?>
        <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xop="http://www.w3.org/2004/08/xop/include" xmlns:ns1="http://cloudnorm.webservice.lbapp.lubansoft.com/" xmlns:ns10="http://webservice.clientcomponent.lbapp.lubansoft.com/" xmlns:ns11="http://webservice.cloudcomponent.lbapp.lubansoft.com/" xmlns:ns12="http://webservice.lbim.lbapp.lubansoft.com/" xmlns:ns13="http://webservice.common.lbapp.lubansoft.com/" xmlns:ns14="http://webservice.costlib.lbapp.lubansoft.com/" xmlns:ns15="http://webservice.usergrade.lbapp.lubansoft.com/" xmlns:ns16="http://webservice.cloudautoset.lbapp.lubansoft.com/" xmlns:ns17="http://webservice.lbcert.lbapp.lubansoft.com/" xmlns:ns18="http://webservice.clientinfo.lbapp.lubansoft.com/" xmlns:ns19="http://webservice.onlineservice.lbapp.lubansoft.com/" xmlns:ns2="http://lbmsg.webservice.lbapp.lubansoft.com/" xmlns:ns20="http://webservice.localbim.lbapp.lubansoft.com/" xmlns:ns21="http://webservice.adimage.lbapp.lubansoft.com/" xmlns:ns22="http://webservice.banbankDrainage.lbapp.lubansoft.com/" xmlns:ns3="http://upgrade.webservice.lbapp.lubansoft.com/" xmlns:ns4="http://cloudpush.webservice.lbapp.lubansoft.com/" xmlns:ns5="http://common.webservice.lbapp.lubansoft.com/" xmlns:ns6="http://clientInfo.webservice.lbapp.lubansoft.com/" xmlns:ns7="http://validate.webservice.lbapp.lubansoft.com/" xmlns:ns8="http://LBUFS.webservice.lbapp.lubansoft.com/" xmlns:ns9="http://webservice.dataserver.LBUFS.lubansoft.com/">
        <SOAP-ENV:Header><LBTag>Kick</LBTag><LBSessionId></LBSessionId></SOAP-ENV:Header>
        <SOAP-ENV:Body>
        <ns6:login>
        <LBLoginParam>
        <computerName>DESKTOP-S2CJPRR</computerName>
        <hardwareCodes>0d80c194d531820c71de04a3998b435e-4ece03d1c7f03a151b241cbd455505ef</hardwareCodes>
        <intranet_IP>172.16.21.178</intranet_IP>
        <lubanNetVersion>4.9.0.5</lubanNetVersion>
        <password>96e79218965eb72c92a549dd5a330112</password>
        <platform>64</platform>
        <productId>3</productId>
        <softwareEnvironment>hostType=CAD;hostVer=2012;OSName=Windows 10;OSBit=64;OSVer=6-2;</softwareEnvironment>
        <username>hubiao</username>
        <version>30.2.1</version>
        </LBLoginParam>
        </ns6:login></SOAP-ENV:Body></SOAP-ENV:Envelope>'''
        response = self.lubansoftLogin.JsonRequest('post',resource,body)
        assert response["status_code"] == 200
        return self.lubansoftLogin

if __name__ == '__main__':
    login = Bimapp("hubiao","264f0c676e143da03019f1698304c468").Login()
