#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/1/2 15:29
# @Author  : hubiao
# @File    : test_LoginBV.py

import time,json,re
import pytest

class Test_LBBV:
    '''
    登录新用户，触发新用户登录PDS产品后自动添加到演示企业
    '''
    @pytest.mark.parametrize('resource,method',[('/rs/bvm/routinginspectionpoint/enterprisersmarks','get')])
    def test_enterprisersmarks(self,LBBV,resource,method):
        # 登录到指定企业
        response = LBBV.JsonRequest(method,resource)
        assert response["status_code"] == 200

    @pytest.mark.parametrize('resource,method',[('/rs/co/priorityList','get')])
    def test_MyLubanAppCollaborationList(self,BimCO,resource,method):
        # 获取优先级
        response = BimCO.JsonRequest(method,resource)
        assert response["status_code"] == 200

    @pytest.mark.parametrize('method', [('get')])
    def test_listApprovalType(self, Process, method):
        # 获取审批类型
        resource = '/approval/common/listApprovalType'
        response = Process.JsonRequest(method, resource)
        assert response["status_code"] == 200

    @pytest.mark.parametrize('method', [('post')])
    def test_pageApprovalForm(self, Process, method):
        # 获取审批
        body = {"searchKey":"","processType":1,"pageParam":{"size":12,"page":1},"requestSource":2}
        resource = '/approval/common/pageApprovalForm'
        response = Process.JsonRequest(method, resource, body)
        assert response["status_code"] == 200

if __name__ == "__main__":
    pytest.main(["-s", "test_LoginBV.py"])