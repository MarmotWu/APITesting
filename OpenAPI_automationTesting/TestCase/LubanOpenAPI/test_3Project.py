#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/2/12 10:27
# @Author  : hubiao
# @File    : test_3Project.py

import pytest,sys
import json
from Common.Config import ManageConfig

class TestProject:
    '''
    工程信息
    '''
    def setup_class(self):
        self.section = 'openapi'
        self.openapi = ManageConfig().getConfig(self.section)
        self.wf = ManageConfig()
        self.ppid = 167619
        self.ppid_list =[]
        self.ppid_baseBuilding_list=[]
        self.ppid_houseBuilding_list=[]

    @pytest.mark.parametrize('method', [('post')])
    def test_dept_proj_infos_all(self, OpenAPIToken, method):
        '''获取项目部下工程列表'''
        #测试外网云部署，WCC迁移数据
        resource = '/rs/orgProjService/dept/proj-infos'
        # 0.房建+基建;1.房建;2.基建
        body = {"type": 0,"deptIds": str(self.openapi["deptid_all_list"]).split(",")}
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        #企业部署
        # assert len(response["data"])>0
        # for value in response['data']:
        #     self.ppid_list.append(value['ppid'])
        #云部署
        assert len(response["data"])>0
        for value in response['data']:
            self.ppid_list.append(value['ppid'])

    @pytest.mark.parametrize('method', [('post')])
    def test_dept_proj_infos_houseBuilding(self, OpenAPIToken, method):
        '''获取项目部下工程列表'''
        resource = '/rs/orgProjService/dept/proj-infos'
        # 0.房建+基建;1.房建;2.基建
        body = {"type": 1,"deptIds": str(self.openapi["deptid_all_list"]).split(",")}
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert len(response["data"])>0
        for value in response["data"]:
            self.ppid_houseBuilding_list.append(value["ppid"])

    @pytest.mark.parametrize('method', [('post')])
    def test_dept_proj_infos_baseBuilding(self, OpenAPIToken, method):
        '''获取项目部下工程列表'''
        resource = '/rs/orgProjService/dept/proj-infos'
        # 0.房建+基建;1.房建;2.基建
        body = {"type": 2,"deptIds": str(self.openapi["deptid_all_list"]).split(",")}
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert len(response["data"])>=0
        for value in response["data"]:
            self.ppid_baseBuilding_list.append(value["ppid"])
        ret_list = list(set(self.ppid_list)^set(self.ppid_houseBuilding_list))
        assert ret_list.sort(reverse=True) == self.ppid_baseBuilding_list.sort(reverse=True)

    @pytest.mark.parametrize('method', [('post')])
    def test_dept_proj_infos_all_failed(self, OpenAPIToken, method):
        '''获取项目部下全部工程列表，部分错误的deptid，失败'''
        resource = '/rs/orgProjService/dept/proj-infos'
        # 0.房建+基建;1.房建;2.基建
        deptIds =[self.openapi["deptid_all"],'errordeptids']
        body = {"type": 0,"deptIds": deptIds}
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response['msg'] == "当前用户没有访问请求资源的权限！"

    @pytest.mark.parametrize('method', [('post')])
    def test_dept_proj_infos_houseBuilding_failed(self, OpenAPIToken, method):
        '''获取项目部下房建工程列表，部分错误的deptid，失败'''
        resource = '/rs/orgProjService/dept/proj-infos'
        # 0.房建+基建;1.房建;2.基建
        deptIds =[self.openapi["deptid_all"],'errordeptids']
        body = {"type": 1,"deptIds": deptIds}
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response['msg'] == "当前用户没有访问请求资源的权限！"

    @pytest.mark.parametrize('method', [('post')])
    def test_dept_proj_infos_baseBuilding_failed(self, OpenAPIToken, method):
        '''获取项目部下工程列表，部分错误的deptid，失败'''
        resource = '/rs/orgProjService/dept/proj-infos'
        # 0.房建+基建;1.房建;2.基建
        deptIds =[self.openapi["deptid_all"],'errordeptids']
        body = {"type": 2,"deptIds": deptIds}
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response['msg'] == "当前用户没有访问请求资源的权限！"

    @pytest.mark.parametrize('method', [('post')])
    def test_proj_details(self, OpenAPIToken, method):
        '''获取工程详情'''
        ppid_list=[]
        resource = '/rs/pdsProject/details'
        body = self.ppid_houseBuilding_list
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        for value in response['data']:
            ppid_list.append(value['ppid'])
            assert value['deptId'] == self.openapi["deptid_all_list"]
            assert value['projModel'] in ['SLYS','SLSG']
            assert value['projType'] in ['土建','安装','钢筋','revit','tekla','Rhino']
        assert list(set(ppid_list)^set(self.ppid_houseBuilding_list)) ==[]

    @pytest.mark.parametrize('method', [('post')])
    def test_proj_details_Failed(self, OpenAPIToken, method):
        '''获取工程详情，部分ppid没有权限'''
        ppid=123321
        resource = '/rs/pdsProject/details'
        body = self.ppid_houseBuilding_list+[ppid]
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response['msg'] == "当前用户没有访问请求资源的权限！"

    @pytest.mark.parametrize('method', [('post')])
    def test_proj_3dfile_Info(self, OpenAPIToken, method):
        '''获取工程三维文件信息'''
        resource = '/rs/pdsProject/3dfile-Info'
        body = self.ppid_houseBuilding_list
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        ppid_list=[value['ppid'] for value in response['data']]
        #for value in response['data']:
        #    assert "downloadSystemFile" in value['address']
        assert list(set(ppid_list)^set(self.ppid_houseBuilding_list))==[]

    @pytest.mark.parametrize('method', [('post')])
    def test_proj_3dfile_Info_Failed(self, OpenAPIToken, method):
        '''获取工程三维文件信息，部分ppid没有权限'''
        ppid='123321'
        resource = '/rs/pdsProject/3dfile-Info'
        body = self.ppid_houseBuilding_list+[ppid]
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response['msg'] == "当前用户没有访问请求资源的权限！"

    @pytest.mark.parametrize('method', [('post')])
    def test_proj_extractfile_list(self, OpenAPIToken, method):
        '''获取工程抽取的文件列表'''
        resource = '/rs/projectdata/project/extractfile-list'
        body = {"ppids":self.ppid_houseBuilding_list,"fileTypes": ["hsfpic","newlbg","hsfpic_big"]}
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    @pytest.mark.parametrize('method', [('post')])
    def test_proj_extractfile_list_Failed(self, OpenAPIToken, method):
        '''获取工程抽取的文件列表，部分ppid没有权限'''
        ppid='123321'
        resource = '/rs/projectdata/project/extractfile-list'
        templist = self.ppid_houseBuilding_list+[ppid]
        body = {"ppids":templist,"fileTypes": ["hsfpic","newlbg","hsfpic_big"]}
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response['msg'] == "当前用户没有访问请求资源的权限！"


if __name__ == "__main__":
    pytest.main(["-s", "test_3Project.py"])