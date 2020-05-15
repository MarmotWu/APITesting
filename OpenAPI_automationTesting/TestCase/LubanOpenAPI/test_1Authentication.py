#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/1/29 13:24
# @Author  : hubiao
# @File    : test_1Authentication.py

import pytest,sys
import json
from Common.Config import ManageConfig


class TestAuthentication:
    '''
    发送微信消息提醒功能
    '''
    def setup_class(self):
        self.section = 'openapi'
        self.openapi = ManageConfig().getConfig(self.section)
        self.wf = ManageConfig()

    @pytest.mark.parametrize('method', [('get')])
    def test_client_login_url(self, OpenAPIToken, method):
        # 获取客户端登录地址
        resource = '/rs/address/client-login-url'
        response = OpenAPIToken.JsonRequest(method, resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response['code'] ==200
        assert response['data'] == "http://app.lbuilder.cn"



    @pytest.mark.parametrize('method', [('get')])
    def test_client_login_url_failed(self, OpenAPIToken, method):
        # 获取客户端登录地址
        resource = '/rs/address/client-login-url'
        response = OpenAPIToken.JsonRequest(method, resource,header={'token':'errorheader'},funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response['code'] ==400
        assert response['msg'] == 'Token验证失败'


    @pytest.mark.parametrize('method', [('post')])
    def test_check_account(self, OpenAPIToken, method):
        # 检查用户登录
        resource = '/rs/user/check-account'
        body = {"username": self.openapi["username"], "password": self.openapi["password"]}
        response = OpenAPIToken.JsonRequest(method, resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response['data'] == 'success'

    @pytest.mark.parametrize('method', [('post')])
    def test_check_account_failedPSW(self, OpenAPIToken, method):
        # 检查用户登录
        password ='errorPassword'
        resource = '/rs/user/check-account'
        body = {"username": self.openapi["username"], "password": password}
        response = OpenAPIToken.JsonRequest(method, resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == '密码错误！'

    @pytest.mark.parametrize('method', [('post')])
    def test_check_account_failedAccount(self, OpenAPIToken, method):
        # 检查用户登录
        Account = 'errorAccount'
        resource = '/rs/user/check-account'
        body = {"username": Account, "password": self.openapi["password"]}
        response = OpenAPIToken.JsonRequest(method, resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == '用户名不存在！'

    @pytest.mark.parametrize('method', [('post')])
    def test_check_account_user_enterprise_info(self, OpenAPIToken, method):
        # 检查用户登录
        Account = 'openapi_tester'
        resource = '/rs/token/user/enterprise-info'
        body = {"username": Account, "password": self.openapi["password"]}
        response = OpenAPIToken.JsonRequest(method, resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        print(response)
        # assert response["code"] == 400
        # assert response["msg"] == '用户名不存在！'

    @pytest.mark.parametrize('method', [('get')])
    def test_check_account_enterprise_info(self, OpenAPIToken, method):
        # 检查用户登录
        #Account = 'sunli'
        resource = '/rs/token/enterprise-info'
        #body = {"username": Account, "password": self.openapi["password"]}
        response = OpenAPIToken.JsonRequest(method, resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        print(response)
        assert response["code"] == 200
        assert response['data']["enterpriseName"] == '指挥中心分公司'

if __name__ == "__main__":
    pytest.main(["-s", "test_1Authentication.py"])
