#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/2/12 16:31
# @Author  : hubiao
# @File    : test_4Component.py

import pytest,sys
import json
from Common.Config import ManageConfig

class TestComponent:
    '''
    构件信息
    '''
    def setup_class(self):
        self.section = 'openapi'
        self.openapi = ManageConfig().getConfig(self.section)
        self.wf = ManageConfig()
        self.ppid = 171954
        self.handle = self.openapi["handle"]
        self.floor = self.openapi["floor"]

    @pytest.mark.parametrize('method', [('post')])
    def test_component_attr(self, OpenAPIToken, method):
        '''获取构件属性接口'''
        resource = '/rs/zsprojectdata/component-attr'
        body = {"ppid": self.ppid,"floor": self.openapi["floor"],"handle": self.handle}
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    @pytest.mark.parametrize('method', [('post')])
    def test_component_attr_failedbyppid(self, OpenAPIToken, method):
        '''获取构件属性接口，ppid无权限或不存在'''
        ppid =123321
        resource = '/rs/zsprojectdata/component-attr'
        body = {"ppid": ppid,"floor": self.openapi["floor"],"handle": self.handle}
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["code"] == 400
        assert response["msg"] == '当前用户没有访问请求资源的权限！'

    @pytest.mark.parametrize('method', [('post')])
    def test_component_attr_failedbyfloor(self, OpenAPIToken, method):
        '''获取构件属性接口,错误的楼层'''
        floor =123321
        resource = '/rs/zsprojectdata/component-attr'
        body = {"ppid": self.ppid,"floor": floor,"handle": self.handle}
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    @pytest.mark.parametrize('method', [('post')])
    def test_component_attr_failedbyhandle(self, OpenAPIToken, method):
        '''获取构件属性接口，错误的构建id'''
        handle =123321
        resource = '/rs/zsprojectdata/component-attr'
        body = {"ppid": self.ppid,"floor": self.openapi["floor"],"handle": handle}
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        #assert response['msg'] == None

    @pytest.mark.parametrize('method', [('post')])
    def test_component_attr_material(self, OpenAPIToken, method):
        '''查询构件材料信息接口'''
        resource = '/rs/zsprojectdata/verify/auth/component-attr/material'
        body = {"ppid": self.ppid,"handle": self.handle,"floor":self.floor}
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    @pytest.mark.parametrize('method', [('post')])
    def test_component_attr_material_failByppid(self, OpenAPIToken, method):
        '''查询构件材料信息接口，不存在或错误的ppid'''
        ppid =123321
        resource = '/rs/zsprojectdata/verify/auth/component-attr/material'
        body = {"ppid": ppid,"handle": self.handle,"floor":self.floor}
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    @pytest.mark.parametrize('method', [('post')])
    def test_component_qrcode(self, OpenAPIToken, method):
        '''获取构件二维码url接口'''
        resource = '/rs/zsprojectdata/verify/auth/component-qrcode'
        body = {"ppid": self.ppid,"floor": self.floor,"handle": self.handle}
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        #assert 'pdscommon' in response["data"]

    @pytest.mark.parametrize('method', [('post')])
    def test_component_qrcode_failByppid(self, OpenAPIToken, method):
        '''获取构件二维码url接口'''
        ppid =123321
        resource = '/rs/zsprojectdata/verify/auth/component-qrcode'
        body = {"ppid": ppid,"floor": self.floor,"handle": self.handle}
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"


    @pytest.mark.parametrize('method', [('post')])
    def test_component_doc(self, OpenAPIToken, method):
        '''获取构件资料接口'''
        resource = '/rs/projectdoc/component'
        body = {"ppid": self.ppid,
                "handleFilter": {"attrName": "一层板（120）","compClass": "板.楼梯","floor": '1',"handle": '16f79fc1-a6b4-44d3-8bc0-523507871b2e',"spec": "","subClass": "现浇板"},
                "param": {"filetype": 1,"keyType": 0,"keyValue": "","projRel": True,"sortCol": "modifytime","sortType": "desc","compGroupRel":False,"compGroupRelType":1,"compGroupId":"","pathIdList":[]},
                "pgInfo": {"currentPage": 1,"pageSize": 100}
                }
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        for value in response['data']['docInfo']:
           assert value['ppid'] == self.ppid

    @pytest.mark.parametrize('method', [('post')])
    def test_component_doc_failByppid(self, OpenAPIToken, method):
        '''获取构件资料接口,错误或者不存在的ppid'''
        ppid = 123321
        resource = '/rs/projectdoc/component'
        body = {"ppid": ppid,
                "handleFilter": {"attrName": "JLQ","compClass": "墙","floor": self.floor,"handle": self.handle,"spec": "","subClass": "剪力墙"},
                "param": {"filetype": 1,"keyType": 0,"keyValue": "","projRel": True,"sortCol": "modifytime","sortType": "desc","compGroupRel":False,"compGroupRelType":1,"compGroupId":"9314a97258e6438791d8b22149be9d11","pathIdList":[]},
                "pgInfo": {"currentPage": 1,"pageSize": 100}
                }
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"


if __name__ == "__main__":
    pytest.main(["-s", "test_4Component.py"])