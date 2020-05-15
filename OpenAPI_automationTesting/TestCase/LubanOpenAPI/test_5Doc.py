#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/2/13 14:27
# @Author  : hubiao
# @File    : test_5Doc.py
import pytest,sys
import json
from Common.Config import ManageConfig

class TestDoc:
    '''
    资料信息
    '''
    def setup_class(self):
        self.section = 'openapi'
        self.openapi = ManageConfig().getConfig(self.section)
        self.wf = ManageConfig()
        self.ppid = 171957
        self.uuid = ''
        self.docid = ''
        self.uuid_list=[]
        self.docid_list=[]

    @pytest.mark.parametrize('method', [('get')])
    def test_directory_trees(self, OpenAPIToken, method):
        '''获取资料目录树结构'''
        resource = '/rs/projectdoc/directory-trees'
        response = OpenAPIToken.JsonRequest(method,resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    @pytest.mark.parametrize('method', [('post')])
    def test_projectdoc_list(self, OpenAPIToken, method):
        '''工程资料列表查询接口'''
        resource = '/rs/projectdoc/project'
        # body = {"ppid": self.openapi["ppid"],"floor": self.openapi["floor"],"handle": self.openapi["handle"]}
        body = {"ppids": [self.ppid],"pathIdList": ["QlKUnmYY"],"fileType":1,"sortCol": "modifytime","sortType": "desc","keyType": 0,"keyValue": "",
                "pgInfo": {"pageSize": 20,"currentPage": 1}
                }
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        for value in response["data"]["docInfo"]:
            self.uuid_list.append(value['uuid'])
            self.docid_list.append(value['docId'])
            assert value['ppid'] == self.ppid

    @pytest.mark.parametrize('method', [('post')])
    def test_projectdoc_list_failByPPid(self, OpenAPIToken, method):
        '''工程资料列表查询接口，有不存在或无权限的ppid'''
        resource = '/rs/projectdoc/project'
        ppid = [self.ppid,123321]
        body = {"ppids": ppid,"pathIdList": [],"fileType": 1,"sortCol": "modifytime","sortType": "desc","keyType": 0,"keyValue": "",
                "pgInfo": {"pageSize": 20,"currentPage": 1}
                }
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    @pytest.mark.parametrize('method', [('post')])
    def test_projectdoc_filetype(self, OpenAPIToken, method):
        '''按文件类型统计工程资料数量及文件大小'''
        ppid = self.ppid
        resource = '/rs/projectdoc/statistic/groupby-filetype'
        body = [ppid]
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    @pytest.mark.parametrize('method', [('post')])
    def test_projectdoc_filetype_failedByPPid(self, OpenAPIToken, method):
        '''按文件类型统计工程资料数量及文件大小,无权限的ppid'''
        ppid = 131939
        resource = '/rs/projectdoc/statistic/groupby-filetype'
        body = [ppid,self.ppid]
        response = OpenAPIToken.JsonRequest(method,resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert response["code"] == 400
        assert response["msg"] == "当前用户没有访问请求资源的权限！"

    # @pytest.mark.parametrize()
    def test_projectdoc_preview(self, OpenAPIToken):
        '''获取资料预览地址'''
        resource = '/rs/projectdoc/preview-url'
        # 资料类别: 1.或者不传为pds资料;2.质检资料
        body = {"ppid": self.ppid,"uuid": 'f8291a077b8e4e45bedc1c6da505259c',"type": 1}
        response = OpenAPIToken.JsonRequest('post',resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200

    # @pytest.mark.parametrize()
    def test_projectdoc_download(self, OpenAPIToken):
        '''获取资料下载地址'''
        resource = '/rs/projectdoc/download-url/'+'f8291a077b8e4e45bedc1c6da505259c'
        response = OpenAPIToken.JsonRequest('get',resource,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200
        assert "http://builder-docsys-server.oss-cn-shanghai.aliyuncs.com" in response['data']

    @pytest.mark.parametrize('relType', [0,5])
    def test_projectdoc_correlate(self, OpenAPIToken, relType):
        '''获取资料关联信息'''
        resource = '/rs/projectdoc/correlate-infos'
        body = {"ppid": self.ppid,"docId": '46a44092-99f1-4cf5-a6ef-9da2b85bbc0a',"relType": relType,"currentPage": 1,"pageSize": 500}
        response = OpenAPIToken.JsonRequest('post',resource, body,funName=sys._getframe().f_code.co_name)
        assert response["status_code"] == 200


if __name__ == "__main__":
    pytest.main(["-s", "test_5Doc.py"])