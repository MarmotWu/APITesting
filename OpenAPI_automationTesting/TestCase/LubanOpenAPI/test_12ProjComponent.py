#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/2/18 14:23
# @Author  : hubiao
# @File    : test_12ProjComponent.py

import pytest,sys
import time
from Common.Config import ManageConfig
from Common.Base import *


class TestProJComponent:
    '''
    工程构件
    '''

    def setup_class(self):
        '''
        定义接口需要用到的字段信息
        '''
        self.wf = ManageConfig()
        self.section = 'openapi'
        self.openapi = ManageConfig().getConfig(self.section)
        self.ppid = 131938
        self.floor = 1
        self.handler = self.openapi["handle"]
        self.componentId = 'd7851b39-aacd-4329-9676-596e429393e9'

    # @pytest.mark.parametrize()
    def test_add_project_component_tree(self, OpenAPIToken):
        '''
        添加构件树
        '''
        resource = '/rs/components/verify/auth/project-component-tree'
        componentId = getStrMD5(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        body = [{"componentId": componentId,"componentName": "构件名"+componentId[0:6],"parentId": "0a28f50c3f8ed541aad24da9cea8ae14"},
                {"componentId": "0a28f50c3f8ed541aad24da9cea8ae14","componentName": "父节点0a28f50","parentId": ""}]
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        TestProJComponent.componentId = componentId

    # @pytest.mark.parametrize()
    def test_project_component_tree(self, OpenAPIToken):
        '''
        获取构件树列表
        '''
        resource = '/rs/components/verify/auth/project-component-tree'
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    @pytest.mark.parametrize('status', [1])
    def test_associate_component(self, OpenAPIToken,status):
        '''
        关联工程构件
        '''
        resource = '/rs/components/verify/auth/associate-project-component'
        # 增加关联：1, 取消关联：0
        body = {"ppid": self.ppid,"componentId": self.componentId,"status": status}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200


if __name__ == '__main__':
    pytest.main(["-s", "test_12ProjComponent.py"])