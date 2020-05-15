#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/2/14 15:35
# @Author  : hubiao
# @File    : test_8BimReportTable.py

import pytest,sys
from Common.Config import ManageConfig

class TestBimReportTable:
    '''
    BIM工程报表接口
    '''

    def setup_class(self):
        '''定义接口需要用到的字段信息'''
        self.wf = ManageConfig()
        self.section = 'openapi'
        self.openapi = ManageConfig().getConfig(self.section)
        self.ppid = 171954
        self.floor = self.openapi["floor"]
        self.handler = self.openapi["handle"]

    # @pytest.mark.parametrize()
    def test_bimReport_qddim_datails(self, OpenAPIToken):
        '''获取算量(土建,安装,钢筋)清单维度条目信息'''
        resource = '/rs/bimReportTable/qddim-datails/'+str(self.ppid)
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    def test_bimReport_qddim_datails_failByppid(self, OpenAPIToken):
        '''获取算量(土建,安装,钢筋)清单维度条目信息,ppid不存在，或者错误'''
        ppid = 0
        resource = '/rs/bimReportTable/qddim-datails/'+str(ppid)
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_bimReport_dedim_datails(self, OpenAPIToken):
        '''获取算量(土建,安装,钢筋)定额条目信息'''
        resource = '/rs/bimReportTable/dedim-datails/'+str(self.ppid)
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_bimReport_dedim_datails_failByppid(self, OpenAPIToken):
        '''获取算量(土建,安装,钢筋)定额条目信息,ppid不存在，或者错误'''
        ppid = 123231
        resource = '/rs/bimReportTable/dedim-datails/'+str(ppid)
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_bimReport_tj_qdde_infos(self, OpenAPIToken):
        '''获取土建工程清单定额信息'''
        resource = '/rs/bimReportTable/tj/qdde-infos'
        body = {"ppid": self.ppid,
                "page": {"currentPage": 1,"pageSize": 2000}
                }
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_bimReport_gj_qdde_infos_failByppid(self, OpenAPIToken):
        '''获取钢筋工程清单定额信息'''
        ppid = 231231
        resource = '/rs/bimReportTable/gj/qdde-infos'
        body = {"ppid": ppid,
                "page": {"currentPage": 1,"pageSize": 2000}
                }
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_bimReport_az_qdde_infos(self, OpenAPIToken):
        '''获取安装工程清单定额信息'''
        resource = '/rs/bimReportTable/az/qdde-infos'
        body = {"ppid": self.ppid,
                "page": {"currentPage": 1,"pageSize": 2000}
                }
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_bimReport_az_qdde_infos_failByppid(self, OpenAPIToken):
        '''获取安装工程清单定额信息'''
        ppid = 23123
        resource = '/rs/bimReportTable/az/qdde-infos'
        body = {"ppid": ppid,
                "page": {"currentPage": 1,"pageSize": 2000}
                }
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_bimReport_revit_qd_infos(self, OpenAPIToken):
        '''获取revit工程清单信息(revit只有清单维度)'''
        resource = '/rs/bimReportTable/revit/qd-infos'
        body = {"ppid": self.ppid,
                "page": {"currentPage": 1,"pageSize": 2000}
                }
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_bimReport_revit_qd_infos_failByppid(self, OpenAPIToken):
        '''获取revit工程清单信息(revit只有清单维度)'''
        ppid = 23123123
        resource = '/rs/bimReportTable/revit/qd-infos'
        body = {"ppid": ppid,
                "page": {"currentPage": 1,"pageSize": 2000}
                }
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"


    # @pytest.mark.parametrize()
    def test_bimReport_proj_floor_infos(self, OpenAPIToken):
        '''获取工程楼层信息接口'''
        resource = '/rs/bimReportTable/proj-floor-infos'
        body = [self.ppid]
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_bimReport_proj_floor_infos_failByppid(self, OpenAPIToken):
        '''获取工程楼层信息接口'''
        ppid = 123321
        resource = '/rs/bimReportTable/proj-floor-infos'
        body = [ppid]
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

if __name__ == '__main__':
    pytest.main(["-s", "test_8BimReportTable.py"])