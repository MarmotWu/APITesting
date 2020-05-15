#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/2/14 16:03
# @Author  : hubiao
# @File    : test_10Govern.py

import pytest,sys
import allure
from Common.Config import ManageConfig

class TestGovern:
    '''
    Govern相关接口
    '''

    def setup_class(self):
        '''定义接口需要用到的字段信息'''
        self.wf = ManageConfig()
        self.section = 'openapi'
        self.openapi = ManageConfig().getConfig(self.section)
        self.ppid = self.openapi['ppid_Govern']
        self.deptId = self.openapi["deptid"]
        self.projType = self.openapi["projType"]
        self.node = self.openapi["node"]
        self.unid = self.openapi["unid_Govern"]
        self.deptId_all = self.openapi["deptid_all_Govern"]
        self.code = self.openapi["code"]
        self.code_rcjSummary = self.openapi["code_rcjSummary"]
        self.uuidkey_qtxm = self.openapi["uuidkey_qtxm"]
        self.uuidkey_gfsj = self.openapi["uuidkey_gfsj"]

    # @pytest.mark.parametrize()
    def test_govern_orgnode_list(self, OpenAPIToken):
        '''
        查询标段、单项、单位工程列表，deptid 是V12.0.0(鲲鹏)
        '''
        resource = '/rs/orgProjService/verify/auth/govern-orgnode-list'
        body = [self.deptId_all]
        node = self.node
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert node in [value['nodeName'] for value in response['data']]

    # @pytest.mark.parametrize()
    def test_govern_orgnode_list_failedByDeptid(self, OpenAPIToken):
        '''
        查询标段、单项、单位工程列表,deptid 无权限
        '''
        resource = '/rs/orgProjService/verify/auth/govern-orgnode-list'
        body = [self.deptId]
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_govern_fbfxdjcs_qd_list_failedByUnid(self, OpenAPIToken):
        '''
        分部分项单价措施合同清单,unid没有权限
        '''
        resource = '/rs/projQuantityService/verify/auth/unitproj/fbfxdjcs-qd-list'
        # 1分部分项 2单价措施
        body = {"unid": '111' ,"type": 2}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_govern_fbfxdjcs_qd_list_1(self, OpenAPIToken):
        '''
        分部分项单价措施合同清单，govern11.4
        '''
        resource = '/rs/projQuantityService/verify/auth/unitproj/fbfxdjcs-qd-list'
        # 1分部分项 2单价措施
        body = {"unid": self.unid ,"type": 1}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response['data'][0]['code'] ==self.code

    # @pytest.mark.parametrize()
    def test_govern_unitproj_values(self, OpenAPIToken):
        '''
        查询单位工程对应的变量值,govern 11.4
        '''
        resource = '/rs/projQuantityService/verify/auth/unitproj/variable-values'
        body = [self.unid]
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert len(response["data"])>0
        assert float(response['data'][0]["money"])>=0

    # @pytest.mark.parametrize()
    def test_govern_fbfxdjcs_qd_list(self, OpenAPIToken):
        '''
        分部分项单价措施合同清单，govern11.4
        '''
        resource = '/rs/projQuantityService/verify/auth/unitproj/fbfxdjcs-qd-list'
        # 1分部分项 2单价措施
        body = {"unid": self.unid ,"type": 1}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 200
        assert response["data"] != []
        assert response['data'][0]['code'] ==self.code

    # # @pytest.mark.parametrize()
    # def test_govern_unitproj_values_1(self, OpenAPIToken):
    #     '''
    #     查询单位工程对应的变量值,govern 11.4
    #     '''
    #     resource = '/rs/projQuantityService/verify/auth/unitproj/variable-values'
    #     body = [self.unid]
    #     response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
    #     assert response["status_code"] == 200
    #     assert response["code"] == 200
    #     assert response["data"] !=[]

    # @pytest.mark.parametrize()
    def test_govern_unitproj_zjcs(self, OpenAPIToken):
        '''
        总价措施,govern11.4
        '''
        unid =self.unid
        resource = '/rs/projQuantityService/verify/auth/unitproj/zjcs/'+unid
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert len(response['data'])>0


    # @pytest.mark.parametrize()
    def test_govern_unitproj_qtxm(self, OpenAPIToken):
        '''
        其他项目清单
        '''
        uuid_list=[]
        resource = '/rs/projQuantityService/verify/auth/unitproj/qtxm/'+str(self.unid)
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert len(response['data'])>0
        for value in list(response['data']):uuid_list.append(value['uuidkey'])
        assert self.uuidkey_qtxm in uuid_list

    # @pytest.mark.parametrize()
    def test_govern_unitproj_gfsj(self, OpenAPIToken):
        '''
        规费及税金
        '''
        uuid_list=[]
        resource = '/rs/projQuantityService/verify/auth/unitproj/gfsj/'+str(self.unid)
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert len(response['data'])>0
        for value in response['data']:uuid_list.append(value['uuidkey'])
        assert self.uuidkey_gfsj in uuid_list

    # @pytest.mark.parametrize()
    def test_govern_project_region_infos(self, OpenAPIToken):
        '''
        查询工程分区(楼层 施工段)信息
        '''
        resource = '/rs/projQuantityService/verify/auth/project/region-infos'
        body = [{"type": self.projType,"ppid": self.ppid}]
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        for value in response['data']: assert str(value['ppid']) ==str(self.ppid)

    # @pytest.mark.parametrize()
    def test_govern_project_classify_infos(self, OpenAPIToken):
        '''
        查询工程构件大小类、构件名称分类信息
        '''
        ppid = self.ppid
        resource = '/rs/projQuantityService/verify/auth/component/classify-infos'
        body = [{"type": self.projType,"ppid": ppid}]
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        for value in response['data']: assert str(value['ppid']) ==str(self.ppid)
        

    # @pytest.mark.parametrize()
    def test_govern_unitproj_statistic_rcjSummary(self, OpenAPIToken):
        '''
        统计人工汇总表/材料汇总表/机械汇总表
        '''
        resource = '/rs/projQuantityService/verify/auth/unitproj/statistic/rcjSummary'
        body = {"unid": self.unid ,"moduleType": 0,"param":None}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert len(response["data"])>0
        assert response['data']['unitQuans'][0]['code'] == self.code_rcjSummary

    def test_govern_unitproj_statistic_rcjSummary_failedByUnid(self, OpenAPIToken):
        '''
        统计人工汇总表/材料汇总表/机械汇总表
        '''
        unid = '111'
        resource = '/rs/projQuantityService/verify/auth/unitproj/statistic/rcjSummary'
        body = {"unid":unid  ,"moduleType": 0,"param":None}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_govern_unitproj_statistic_qdrcjSummary(self, OpenAPIToken):
        '''
        统计分部分项清单和人材机结果集
        '''
        resource = '/rs/projQuantityService/verify/auth/unitproj/statistic/qdrcjSummary'
        body ={"unid":self.unid  ,"moduleType": 0,"param":None}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert len(response["data"])>0
        assert response['data']['unitQuans'][0]['code'] == self.code

    # @pytest.mark.parametrize()
    def test_govern_unitproj_statistic_qdrcjSummary_failedByUnid(self, OpenAPIToken):
        '''
        统计分部分项清单和人材机结果集
        '''
        unid = '333'
        resource = '/rs/projQuantityService/verify/auth/unitproj/statistic/qdrcjSummary'
        body ={"unid":unid  ,"moduleType": 0,"param":None}
        response = OpenAPIToken.JsonRequest('post', resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_govern_unitproj_gljprice(self, OpenAPIToken):
        '''
        查询综合单价工料机分析表数据
        '''
        price_list=[]
        resource = '/rs/projQuantityService/verify/auth/unitproj/gljprice/'+str(self.unid)
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert len(response['data'])>0
        for value in response['data']:assert float(value['price'])>=0


    # @pytest.mark.parametrize()
    def test_govern_unitproj_price(self, OpenAPIToken):
        '''
        查询综合单价分析表
        '''
        resource = '/rs/projQuantityService/verify/auth/unitproj/price/'+str(self.unid)
        response = OpenAPIToken.JsonRequest('get', resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert len(response['data'])>0
        assert response['data'][0]['code'] == self.code

if __name__ == '__main__':
    pytest.main(["-s", "test_10Govern.py"])