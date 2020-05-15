#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2018/8/1 16:03
# @Author  : hubiao
# @File    : test_BimAdamin.py

import time,json
import pytest
from Common.Config import ManageConfig

section = 'sysadmin'
rf = ManageConfig().getConfig(section)
wf = ManageConfig()
username = 'lbtest' + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

class Test_BimAdmin:
    '''
    登录运营系统后台，并添加一个新用户，用来测试新用户添加到演示企业的场景
    '''
    @pytest.mark.parametrize('resource,method', [('/LBAdmin/usermanager/getUserMessagePage.htm', 'post')])
    def test_queryUser(self,BimAadminLogin,resource,method):
        '''
        查询用户是否存在
        :param BimAadminLogin:
        :return:
        '''
        body = {"sortInfo": {"sortColumns": "regdate", "sortType": "1"},
                "pageInfo": {"currentPage": 1, "pageSize": "25"},
                "type": "1", "mobileType": "0", "searchWord": ""}
        body['searchWord'] = username
        response = BimAadminLogin.JsonRequest(method,resource,body)
        response = json.loads(response["data"].replace('/', ''))
        totalNumber = response[0]["result"]["totalNumber"]
        assert totalNumber <= 0

    @pytest.mark.parametrize('resource,method', [('/LBAdmin/usermanager/batchAddLubanAccount.htm', 'post')])
    def test_addUser(self,BimAadminLogin,resource,method):
        '''
        添加用户
        :param BimAadminLogin:
        :return:
        '''
        body = {"userArray":[{"username":"","password":"96e79218965eb72c92a549dd5a330112","email":"","mobile":""}]}
        body['userArray'][0]['username'] = username
        body['userArray'][0]['email'] = username+"@qq.com"
        response = BimAadminLogin.JsonRequest(method,resource,body)
        assert response["status_code"] == 200
        response = json.loads(response["data"].replace('/', ''))
        result = response[0]["type"]
        assert result == "success"
        #把用户写入配置表
        wf.writeConfig(section, 'newUserName', username)

if __name__ == "__main__":
    pytest.main(["-s", "test_BimAdamin.py"])
