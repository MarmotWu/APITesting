#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/2/14 13:32
# @Author  : hubiao
# @File    : test_7Collaboration.py

import pytest,sys
from Common.Config import ManageConfig

class TestCollaboration:
    '''
    测试类名
    '''

    def setup_class(self):
        '''定义接口需要用到的字段信息'''
        self.wf = ManageConfig()
        self.section = 'openapi'
        self.openapi = ManageConfig().getConfig(self.section)
        self.ppid = 168009
        self.floor = self.openapi["floor"]
        self.handler = self.openapi["handle"]
        self.coid = ''
        self.typeId = ''
        self.typeId_list = []
        self.coid_list = []

    # @pytest.mark.parametrize()
    def test_collaboration_type_list(self, OpenAPIToken):
        '''企业协同类型列表'''
        resource = '/rs/collaboration/type-list'
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        #hastypeId = False
        for cotype in response["data"]:
            assert cotype["typeId"]!=None and cotype["typeId"]!=""
            self.typeId_list.append(cotype["typeId"])

    # @pytest.mark.parametrize()
    def test_collaboration_statistic_count_groupby_type(self, OpenAPIToken):
        '''统计协同各问题类型数量'''
        name='问题整改'
        resource = '/rs/collaboration/verify/auth/statistic-count-groupby-type'
        body = {"startTime": None,"endTime": None}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        name_list = [value['name'] for value in response['data']]
        type_list = [value['type'] for value in response['data']]
        assert type_list[name_list.index(name)] ==1


    # @pytest.mark.parametrize()
    def test_collaboration_type_co_list(self, OpenAPIToken):
        '''获取指定类型协作列表'''
        resource = '/rs/collaboration/verify/auth/co-list-by-type'
        body = {"typeId": self.typeId_list[0],"modifyTime": None,"modifyTimeCount": 0,"count": 20}
        response = OpenAPIToken.JsonRequest('post', resource, body)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_collaboration_proj_count_groupby_type(self, OpenAPIToken):
        '''按协作类型统计工程关联协作数量'''
        resource = '/rs/collaboration/proj-correlate/statistic-count-groupby-type'
        body = [self.ppid]
        typeId = '5b2a6d70003210f5ea0760ef'
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert len(response['data'])>0
        assert typeId in [value['typeId'] for value in response['data']]

    # @pytest.mark.parametrize()
    def test_collaboration_proj_count_groupby_type_failedByppid(self, OpenAPIToken):
        '''按协作类型统计工程关联协作数量'''
        resource = '/rs/collaboration/proj-correlate/statistic-count-groupby-type'
        body = [131993]
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_collaboration_proj_count_groupby_state(self, OpenAPIToken):
        '''按协作状态统计协作数量'''
        resource = '/rs/collaboration/statistic-count-groupby-state'
        body = [self.ppid]
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert len(response['data'])>0

    # @pytest.mark.parametrize()
    def test_collaboration_proj_count_groupby_state_failedbyPPid(self, OpenAPIToken):
        '''按协作状态统计协作数量'''
        resource = '/rs/collaboration/statistic-count-groupby-state'
        body = [131993]
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_collaboration_ppids_count(self, OpenAPIToken):
        '''统计协作总数'''
        resource = '/rs/collaboration/statistic-count'
        body = {"ppids": [self.ppid],"startTime": None,"endTime": None}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response['data']>0

    # @pytest.mark.parametrize()
    def test_collaboration_ppids_count_failedByppid(self, OpenAPIToken):
        '''统计协作总数'''
        resource = '/rs/collaboration/statistic-count'
        body = {"ppids": [131993,self.ppid],"startTime": None,"endTime": None}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_collaboration_list(self, OpenAPIToken):
        '''分页获取协作列表'''
        resource = '/rs/collaboration/page-list'
        coid = '5d391c08e4b03725833ed03c'
        body = {"ppids": [self.ppid],
                "handle": None,"searchKey": None,
                "typeIds": [],
                "modifyTime": 0,"modifyTimeCount": 0,"count": 0}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        for value in response['data']:self.coid_list.append(value["coid"])
        assert coid in self.coid_list

    # @pytest.mark.parametrize()
    def test_collaboration_list_failedByPPid(self, OpenAPIToken):
        '''分页获取协作列表'''
        resource = '/rs/collaboration/page-list'
        coid = '5cd11d4984aed199d42030b3'
        body = {"ppids": [131993,self.ppid],
                "handle": None,"searchKey": None,
                "typeIds": [],
                "modifyTime": 0,"modifyTimeCount": 0,"count": 0}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_collaboration_detail(self, OpenAPIToken):
        '''企业协同类型列表'''
        name = '质量-190725'
        resource = '/rs/collaboration/verify/auth/detail/'+str(self.coid_list[0])
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response['data']["name"] == name

    # @pytest.mark.parametrize()
    def test_collaboration_detail_failedByCoid(self, OpenAPIToken):
        '''企业协同类型列表'''
        coid = '123321'
        resource = '/rs/collaboration/verify/auth/detail/'+coid
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 300
        assert response["msg"] == "当前协作不存在或已删除"

    # @pytest.mark.parametrize()
    def test_collaboration_count_endstate(self, OpenAPIToken):
        '''按协作结束状态统计协作数量'''
        resource = '/rs/collaboration/verify/auth/statistic-count-groupby-endstate'
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_collaboration_proj_count_groupby_component(self, OpenAPIToken):
        '''按工程构件分组统计协作数量'''
        resource = '/rs/collaboration/verify/auth/statistic-count-groupby-component'
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200


if __name__ == '__main__':
    pytest.main(["-s", "test_7Collaboration.py"])