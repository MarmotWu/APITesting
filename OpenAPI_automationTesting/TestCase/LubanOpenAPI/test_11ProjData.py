#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/2/18 11:22
# @Author  : hubiao
# @File    : test_11ProjData.py

import pytest,sys
from Common.Config import ManageConfig


class TestProjData:
    '''
    测试类名
    '''

    def setup_class(self):
        '''
        定义接口需要用到的字段信息
        '''
        self.wf = ManageConfig()
        self.section = 'openapi'
        self.openapi = ManageConfig().getConfig(self.section)
        self.ppid = 171954
        self.floor = self.openapi["floor"]
        self.handler = self.openapi["handle"]
        self.projType = self.openapi["projType"]

    # @pytest.mark.parametrize()
    def test_project_qdquantity_infos(self, OpenAPIToken):
        '''
        测试用例或接口名称
        '''
        resource = '/rs/projectdata/verify/auth/project/qdquantity-infos'
        body = {"ppid": self.ppid,
                "projType": self.projType,
                "handles": None}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_project_qdquantity_infos_failedByPPid(self, OpenAPIToken):
        '''
        测试用例或接口名称
        '''
        resource = '/rs/projectdata/verify/auth/project/qdquantity-infos'
        body = {"ppid": 33,
                "projType": self.projType,
                "handles": None}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_project_qdquantity_infos_failedByppid(self, OpenAPIToken):
        '''
        测试用例或接口名称
        '''
        ppid = 321123
        resource = '/rs/projectdata/verify/auth/project/qdquantity-infos'
        body = {"ppid": ppid,
                "projType": self.projType,
                "handles": [{"floor": self.floor,"handle": self.handler}]}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_project_swl_infos(self, OpenAPIToken):
        '''
        测试用例或接口名称
        '''
        resource = '/rs/projectdata/verify/auth/project/swl-infos'
        body = {"ppid": self.ppid,
                "projType": self.projType,
                "handles": [{"floor": self.floor,"handle": self.handler}]}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_project_swl_infos_failedByppid(self, OpenAPIToken):
        '''
        测试用例或接口名称
        '''
        resource = '/rs/projectdata/verify/auth/project/swl-infos'
        body = {"ppid": 1676191,
                "projType": self.projType,
                "handles": [{"floor": self.floor,"handle": self.handler}]}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_project_qd_infos(self, OpenAPIToken):
        '''
        查询工程清单信息列表
        '''
        resource = '/rs/projectdata/verify/auth/project/qd-list'
        body = {"ppid": self.ppid,"projType": self.projType}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_project_component_list(self, OpenAPIToken):
        '''
        获取工程构件信息列表(直到返回的数组长度为0结束)
        '''
        resource = '/rs/projectdata/verify/auth/project/component-list'
        body = {"ppid": self.ppid,"scrollKey": None}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200


if __name__ == '__main__':
    pytest.main(["-s", "test_11ProjData.py"])