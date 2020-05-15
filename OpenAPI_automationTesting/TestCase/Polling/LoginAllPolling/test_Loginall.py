#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/3/5 17:44
# @Author  : hubiao
# @File    : test_Loginall.py
import sys
import allure
import pytest
import json
from Common.Config import ManageConfig
from Common import Base

@allure.feature("全产品登录检查")
class TestLogin:
    '''
    测试类名
    '''

    def setup_class(self):
        '''
        定义接口需要用到的字段信息
        '''
        self.wf = ManageConfig()

    @pytest.mark.parametrize('resource,method', [('/org/nodes', 'get')])
    @allure.story("Center登录")
    def test_Center_Login(self, CenterBuilder, resource, method):
        '''
        Center_Login获取组织节点
        '''
        response = CenterBuilder.JsonRequest(method, resource)
        assert response["status_code"] == 200
        if response["code"] == 200 and len(response["data"]) != 0:
            assert True
        else:
            assert False

    @allure.story("Myluban app LBBV登录")
    @pytest.mark.parametrize('resource,method', [('/rs/bvm/routinginspectionpoint/enterprisersmarks', 'get')])
    def test_MylubanApp_LBBV_Login(self, LBBV, resource, method):
        '''
        MylubanApp_LBBV_Login LBBV项目登录
        '''
        response = LBBV.JsonRequest(method, resource)
        assert response["status_code"] == 200

    @allure.story("Myluban app CO登录")
    @pytest.mark.parametrize('resource,method',[('/rs/co/priorityList','get')])
    def test_MyLubanApp_BimCO_Login(self,BimCO,resource,method):
        '''
        MMyLubanApp_BimCO_Login BIMCO项目登录
        '''
        response = BimCO.JsonRequest(method,resource)
        assert response["status_code"] == 200

    @allure.story("Myluban app Process登录")
    @pytest.mark.parametrize('method', [('get')])
    def test_MyLubanApp_Process_Login(self, Process, method):
        '''
        MMyLubanApp_Process_Login 审批项目登录
        '''
        resource = '/approval/common/listApprovalType'
        response = Process.JsonRequest(method, resource)
        assert response["status_code"] == 200

    @allure.story("运维后台登录")
    @pytest.mark.parametrize('resource,method', [('/LBAdmin/usermanager/getUserMessagePage.htm', 'post')])
    def test_BimAdmin_Login(self, BimAadminLogin, resource, method):
        '''
        BimAdmin_Login 获取用户列表
        '''
        body = {"sortInfo": {"sortColumns": "regdate", "sortType": "1"},
                "pageInfo": {"currentPage": 1, "pageSize": "25"},
                "type": "1", "mobileType": "0", "searchWord": "hubiao13916829124"}
        response = BimAadminLogin.JsonRequest(method, resource, body)
        response = json.loads(response["data"].replace('/', ''))
        totalNumber = response[0]["result"]["totalNumber"]
        assert totalNumber <= 0

    @allure.story("Bimapp登录")
    @pytest.mark.parametrize('resource,method', [('/user/myservice/info/lubangift/queryLubanGiftList.htm', 'post')])
    def test_BimApp_Login(self, BimAppLogin, resource, method):
        '''
        BimApp_Login 获取用户套餐
        '''
        body = {"pagedInfo":{"rows":25,"page":1},"sortInfo":{"sortColumns":"receiveTime","sortType":1},"isAuthMobile":True,"queryType":1}
        response = BimAppLogin.JsonRequest(method, resource, body)
        response = json.loads(response["data"].replace('/', ''))
        result = response[0]["type"]
        assert result == "success"

    @allure.story("Myluban web登录")
    @pytest.mark.parametrize('resource,method', [('/myluban/rest/user/unread/messages/nums', 'get')])
    def test_MylubanWeb_Login(self, MylubanWebLogin, resource, method):
        '''
        MylubanWeb_Login 获取消息数量
        '''
        response = MylubanWebLogin.JsonRequest(method, resource)
        assert response["code"] == 1

    @allure.story("业务管理系统登录")
    def test_Bussiness_Login(self, BussinessLogin):
        '''
        Bussiness_Login 查询指定日间的企业数量
        '''
        resource = f'/rest/enterprise/general/queryEntQuantity/{Base.getUnix()}'
        response = BussinessLogin.JsonRequest('get', resource)
        assert response["code"] == 0

    @allure.story("算量登录")
    def test_lubansoft_Login(self):
        '''
        ShuanLiang_Login查询用户是否存在
        '''
        from suds.client import Client
        self.section = 'lubansoft'
        self.lubansoft = ManageConfig().getConfig(self.section)
        self.host = self.lubansoft["host"]
        self.username = self.lubansoft["username"]
        self.password = self.lubansoft["password"]
        loginParameter = {"computerName": "DESKTOP-S2CJPRR",
                          "hardwareCodes": "0d80c194d531820c71de04a3998b435e-4ece03d1c7f03a151b241cbd455505ef",
                          "intranet_IP": "172.16.21.178",
                          "lubanNetVersion": "4.9.0.5",
                          "password": self.password,
                          "platform": "64",
                          "productId": "3",
                          "softwareEnvironment": "hostType=CAD;hostVer=2012;OSName=Windows 10;OSBit=64;OSVer=6-2;",
                          "username": self.username,
                          "version": "30.2.1"}
        loginWSDL = Client(f'{self.host}/webservice/clientInfo/LBClient?wsdl')
        res = loginWSDL.service.login(loginParameter)
        assert res["isValidated"] is True


if __name__ == '__main__':
    pytest.main(["-s", "test_Loginall.py"])