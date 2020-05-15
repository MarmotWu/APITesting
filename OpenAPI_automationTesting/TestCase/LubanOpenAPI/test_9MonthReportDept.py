#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/2/14 15:54
# @Author  : hubiao
# @File    : test_9MonthReportDept.py

import pytest,sys
from Common.Config import ManageConfig

class TestMonthReportDept:
    '''
     项目部月报表
    '''

    def setup_class(self):
        '''定义接口需要用到的字段信息'''
        self.wf = ManageConfig()
        self.section = 'openapi'
        self.openapi = ManageConfig().getConfig(self.section)
        self.deptId = '846f74592e5e4824b80a113058d67f67'

    # @pytest.mark.parametrize()
    def test_monthReportDept_factcost(self, OpenAPIToken):
        '''按月获取项目部的月实际成本'''
        resource = '/rs/monthReportDept/factcost/month-infos/'+str(self.deptId)
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_monthReportDept_factcost_failedByDeptid(self, OpenAPIToken):
        '''按月获取项目部的月实际成本,错误的deptid'''
        deptid = '321231'
        resource = '/rs/monthReportDept/factcost/month-infos/'+deptid
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_monthReportDept_factincome(self, OpenAPIToken):
        '''按月获取项目部的实际收入'''
        resource = '/rs/monthReportDept/factincome/month-infos/'+str(self.deptId)
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_monthReportDept_factincome_failedByDeptid(self, OpenAPIToken):
        '''按月获取项目部的实际收入'''
        deptId = '1111111'
        resource = '/rs/monthReportDept/factincome/month-infos/'+deptId
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_monthReportDept_plancost(self, OpenAPIToken):
        '''按月获取项目部的计划成本'''
        resource = '/rs/monthReportDept/plancost/month-infos/'+str(self.deptId)
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_monthReportDept_plancost_failedByDeptid(self, OpenAPIToken):
        '''按月获取项目部的计划成本'''
        deptId = '321123'
        resource = '/rs/monthReportDept/plancost/month-infos/'+deptId
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_monthReportDept_planincome(self, OpenAPIToken):
        '''按月获取项目部的计划收入'''
        resource = '/rs/monthReportDept/planincome/month-infos/'+str(self.deptId)
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_monthReportDept_planincome_failedByDeptid(self, OpenAPIToken):
        '''按月获取项目部的计划收入'''
        deptId = '321123'
        resource = '/rs/monthReportDept/planincome/month-infos/'+deptId
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_monthReportDept_time_scope(self, OpenAPIToken):
        '''项目部下的月报的最小开始时间和最大结束时间'''
        resource = '/rs/monthReportDept/time-scope/'+str(self.deptId)
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert len(response['data'])>0

    # @pytest.mark.parametrize()
    def test_monthReportDept_time_scope_failedByDeptid(self, OpenAPIToken):
        '''项目部下的月报的最小开始时间和最大结束时间'''
        deptId = '32112312'
        resource = '/rs/monthReportDept/time-scope/'+deptId
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"


if __name__ == '__main__':
    pytest.main(["-s", "test_9MonthReportDept.py"])