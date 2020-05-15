#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/2/14 9:52
# @Author  : hubiao
# @File    : test_6Schedule.py
import pytest,sys
import json
from Common.Config import ManageConfig

class TestSchedule:
    '''
    进度信息
    '''
    def setup_class(self):
        '''定义接口需要用到的字段信息'''
        self.section = 'openapi'
        self.openapi = ManageConfig().getConfig(self.section)
        self.wf = ManageConfig()
        self.ppid = 171954
        self.floor = self.openapi["floor"]
        self.handler = self.openapi["handle"]

    # @pytest.mark.parametrize()
    def test_timescope_plan(self, OpenAPIToken):
        '''获取工程计划进度的开始时间和结束时间'''
        resource = '/rs/planschedule/project/timescope'
        body = [self.ppid]
        response = OpenAPIToken.JsonRequest('post',resource,body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200


    # @pytest.mark.parametrize()
    def test_timescope_plan_failbyppid(self, OpenAPIToken):
        '''获取工程计划进度的开始时间和结束时间,错误或者无权限的ppid'''
        resource = '/rs/planschedule/project/timescope'
        body = [332211]
        response = OpenAPIToken.JsonRequest('post',resource,body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_timescope_be(self, OpenAPIToken):
        '''工程沙盘进度的开始时间和结束时间'''
        resource = '/rs/sandtable/project/timescope'
        body = [self.ppid]
        response = OpenAPIToken.JsonRequest('post',resource,body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        # assert response['data'][0]["ppid"] == self.ppid
        # assert response['data'][0]["startTime"] !=None and response['data'][0]["startTime"] !=""
        # assert response['data'][0]["endTime"] !=None and response['data'][0]["endTime"] !=""

    # @pytest.mark.parametrize()
    def test_timescope_be_failbyppid(self, OpenAPIToken):
        '''工程沙盘进度的开始时间和结束时间,错误或者无权限的ppid'''
        resource = '/rs/sandtable/project/timescope'
        body = [self.ppid,321]
        response = OpenAPIToken.JsonRequest('post',resource,body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_project_statetree(self, OpenAPIToken):
        '''查询指定工程的状态树结构'''
        resource = '/rs/state/verify/auth/statetree/'+str(self.ppid)
        response = OpenAPIToken.JsonRequest('get',resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        #assert len(response['data']['subNodes'])>0


    # @pytest.mark.parametrize()
    def test_project_statetree_failedByPPid(self, OpenAPIToken):
        '''查询指定工程的状态树结构,传入错误的ppid'''
        ppid = '123'
        resource = '/rs/state/verify/auth/statetree/'+str(ppid)
        response = OpenAPIToken.JsonRequest('get',resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_all_component_states(self, OpenAPIToken):
        '''分页查询工程所有构件的状态信息'''
        resource = '/rs/state/verify/auth/all-component-states'
        body = {"ppid": self.ppid,"startTime": "","endTime": "",
                "ck": None,
                "limit": 20}
        response = OpenAPIToken.JsonRequest('post',resource,body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_all_component_states_failbyppid(self, OpenAPIToken):
        '''分页查询工程所有构件的状态信息'''
        ppid = 321123
        resource = '/rs/state/verify/auth/all-component-states'
        body = {"ppid": ppid,"startTime": "","endTime": "",
                "ck": None,
                "limit": 20}
        response = OpenAPIToken.JsonRequest('post',resource,body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_singlecomponent_states(self, OpenAPIToken):
        '''查询单个构件状态信息'''
        resource = '/rs/state/verify/auth/singlecomponent-states'
        body = {"ppid": self.ppid,
                "compKey": {"floor": self.floor,"compHandler": self.handler}
                }
        response = OpenAPIToken.JsonRequest('post',resource,body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_singlecomponent_states_failbyppid(self, OpenAPIToken):
        '''查询单个构件状态信息'''
        ppid = 321123
        resource = '/rs/state/verify/auth/singlecomponent-states'
        body = {"ppid": ppid,
                "compKey": {"floor": self.floor,"compHandler": self.handler}
                }
        response = OpenAPIToken.JsonRequest('post',resource,body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

if __name__ == "__main__":
    pytest.main(["-s", "test_6Schedule.py"])