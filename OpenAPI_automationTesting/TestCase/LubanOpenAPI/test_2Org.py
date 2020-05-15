#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/1/30 15:49
# @Author  : hubiao
# @File    : test_2Org.py

import pytest,sys
import json
from Common.Config import ManageConfig

class TestOrg:
    '''
    组织信息
    '''
    def setup_class(self):
        self.section = 'openapi'
        self.openapi = ManageConfig().getConfig(self.section)
        self.wf = ManageConfig()
        self.deptId_list = []
        self.orgId = ""

    @pytest.mark.parametrize('method', [('get')])
    def test_org_dept_list(self, OpenAPIToken, method):
        '''获取组织项目部列表'''
        resource = '/rs/orgProjService/org-dept-list'
        response = OpenAPIToken.JsonRequest(method, resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 200
        #企业部署
        assert response['data']["orgName"] != None
        #云部署
        # assert response['data']["orgName"] == 'lb9124oo的企业'
        for org in response["data"]["childList"]:
            if not org["childList"] and org["orgType"] == 2:
                self.deptId_list.append(org["orgId"])
            else:
                for org in org["childList"]:
                    if not org["childList"] and org["orgType"] == 2:
                        self.deptId_list.append(org["orgId"])
        assert len(self.deptId_list)!=0,'没有项目部'

    @pytest.mark.parametrize('method', [('get')])
    def test_org_dept_list_failed(self, OpenAPIToken, method):
        '''获取组织项目部列表'''
        resource = '/rs/orgProjService/org-dept-list'
        response = OpenAPIToken.JsonRequest(method, resource,header={'token':'errorheader'},funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response['code'] == 400
        assert response['msg'] == "Token验证失败"

    @pytest.mark.parametrize('method', [('get')])
    def test_check_account(self, OpenAPIToken, method):
        '''获取项目部详情'''
        resource = r'/rs/deptInfo/detail/'+self.deptId_list[0]
        response = OpenAPIToken.JsonRequest(method,resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["data"]['deptId'] == self.deptId_list[0]
        #企业部署
        # assert response["data"]['deptName'] == '初始化项目部'
        #云部署
        #assert response["data"]['deptName'] == 'Govern12.0.0'

    @pytest.mark.parametrize('method', [('get')])
    def test_check_account_failedByDepteid(self, OpenAPIToken, method):
        '''获取项目部详情'''
        deptId = '333222111'
        resource = r'/rs/deptInfo/detail/'+deptId
        response = OpenAPIToken.JsonRequest(method,resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    @pytest.mark.parametrize('method', [('get')])
    def test_check_account_branchOffice_failedByDeptid(self, OpenAPIToken, method):
        '''获取项目部详情,分公司信息不返回，orgid =1'''
        #云部署
        deptId = 'ed0ec6718220450bbc3a7c7bf3fd6b3d'
        resource = r'/rs/deptInfo/detail/'+deptId
        response = OpenAPIToken.JsonRequest(method,resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    @pytest.mark.parametrize('method', [('get')])
    def test_check_account_failed(self, OpenAPIToken, method):
        '''获取项目部详情,错误的deptid'''
        deptId ="12332dsasdasdasd1231231231231231231231"
        resource = r'/rs/deptInfo/detail/'+deptId
        response = OpenAPIToken.JsonRequest(method,resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

if __name__ == "__main__":
    pytest.main(["-s", "test_2Org.py"])