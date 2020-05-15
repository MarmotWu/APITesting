#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2018/8/1 16:03
# @Author  : hubiao
# @File    : test_extractProj.py

import time,json,re
import pytest
from Common.Config import ManageConfig
import allure

@allure.feature("抽取工程是否正常")
class Test_extract:
    '''
    登录企业，查询工程并抽取工程，确认抽取服务器是否正常
    '''
    def setup_class(self):
        self.wf = ManageConfig()
        self.projId = ''


    # def nodes(self,CenterBuilder):
    #     '''
    #     登录Builder用，第一个接口必须要是get接口
    #     '''
    #     resource = '/org/nodes'
    #     response = CenterBuilder.JsonRequest('get',resource)
    #     assert response["status_code"] == 200
    #
    #
    # def getProjects(self,CenterBuilder):
    #     '''
    #     获取工程列表
    #     '''
    #     body = {"operator":"","delete":False,"deptIds":[],"latest":True,"packageType":1,
    #             "pageParam":{"orders":[{"direction":1,"ignoreCase":True,"property":"t1.updateDate"}],"page":1,"size":10},"projGenre":None,"projType":0,"searchKey":"抽取测试工程（勿删）180622","skOnlyProjName":False}
    #     response = CenterBuilder.JsonRequest('post',resource,body)
    #     assert response["status_code"] == 200
    #     assert response["code"] == 200
    #     assert response["success"] == True
    #     if response["data"]["totalElements"] >= 1:
    #         Test_extract.projId = response["data"]['content'][0].get('projId')
    #     else:
    #         assert False

    @allure.story("抽取工程")
    @allure.issue("BUG号：123")  # 问题表识，关联标识已有的问题，可为一个url链接地址
    @allure.testcase("用例名：测试字符串相等")  # 用例标识，关联标识用例，可为一个url链接地址
    @allure.step("字符串相加")  # 测试步骤，通过{0}，{1}可以取到函数传参
    def test_extractProj(self,CenterBuilder):
        '''
        抽取工程
        '''
        with allure.step("第一个接口必须要是get接口，获取组织列表"):
            allure.attach('期望结果', '添加购物车成功')
            resource = '/org/nodes'
            response = CenterBuilder.JsonRequest('get', resource)
            assert response["status_code"] == 200
        with allure.step("获取工程列表"):
            resource = '/rs/bimRest/getProjects'
            body = {"operator":"","delete":False,"deptIds":[],"latest":True,"packageType":1,
                    "pageParam":{"orders":[{"direction":1,"ignoreCase":True,"property":"t1.updateDate"}],"page":1,"size":10},"projGenre":None,"projType":0,"searchKey":"抽取测试工程（勿删）180622","skOnlyProjName":False}
            response = CenterBuilder.JsonRequest('post',resource,body)
            assert response["status_code"] == 200
            assert response["code"] == 200
            assert response["success"] == True
            if response["data"]["totalElements"] >= 1:
                Test_extract.projId = response["data"]['content'][0].get('projId')
            else:
                assert False
        with allure.step("抽取工程"):
            assert self.projId != ''
            resource = f'/rs/bimRest/extractProj/{self.projId}/1'
            response = CenterBuilder.JsonRequest('get',resource)
            assert response["status_code"] == 200
            assert response["code"] == 200
            assert response["success"] == True
            '''
            循环获取工程列表判断是否抽取成功
            '''
            resource = '/rs/bimRest/getProjects'
            body = {"operator":"","delete":False,"deptIds":[],"latest":True,"packageType":1,
                    "pageParam":{"orders":[{"direction":1,"ignoreCase":True,"property":"t1.updateDate"}],"page":1,"size":10},"projGenre":None,"projType":0,"searchKey":"抽取测试工程（勿删）180622","skOnlyProjName":False}
            ageing = 0
            while 1:
                response = CenterBuilder.JsonRequest('post',resource,body)
                assert response["status_code"] == 200
                assert response["code"] == 200
                assert response["success"] == True
                # 判断status为1时，表示抽取成功
                if response["data"]["totalElements"] >= 1 and response["data"]['content'][0].get('status') == 1:
                    break
                ageing+=1
                # 等待5秒
                time.sleep(5)
                if ageing > 120:
                    assert False,"抽取超时(超过10分钟未处理完)"


if __name__ == "__main__":
    pytest.main(["-s", "test_extractProj.py"])
