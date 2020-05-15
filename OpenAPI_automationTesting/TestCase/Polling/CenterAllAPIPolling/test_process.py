#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/4/1 10:58
# @Author  : hubiao
# @File    : test_process.py

import pytest
from Common.Config import ManageConfig


class TestDoc:
    '''
    测试类名
    '''

    def setup_class(self):
        '''
        定义接口需要用到的字段信息
        '''
        self.wf = ManageConfig()
        self.section = 'openapi'
        self.openapi = ManageConfig().getConfig(self.section)
        self.orgId = ''


    def test_jump(self,CenterProcess):
        '''
        Process 302跳转接口
        '''
        resource = '/process/jump'
        response = CenterProcess.JsonRequest('get',resource)
        assert response["status_code"] == 200

    def test_templates(self, CenterProcess):
        '''
        获取流程类型模板列表
        '''
        resource = '/process/templates'
        body = {"page":1,"size":10,"orders":[{"property":"updateTime","direction":1}],"keyword":""}
        response = CenterProcess.JsonRequest('post', resource, body)
        assert response["status_code"] == 200

    def test_proc_form_tmpl(self, CenterProcess):
        '''
        新建流程类型模板
        '''
        resource = '/process/proc_form_tmpl'
        body = {
  "formTmpl": {
    "components": [
      [
        {
          "booleanAttributes": [
            {
              "name": "REQUIRED",
              "value": True
            }
          ],
          "id": "f866f6020458477495d09f28a7680011",
          "stringAttributes": [
            {
              "name": "TITLE",
              "value": "标题"
            },
            {
              "name": "PLACE_HOLDER",
              "value": "请输入标题(必填)"
            }
          ],
          "type": "SINGLE_LINE_TEXT"
        },
        {
          "booleanAttributes": [
            {
              "name": "REQUIRED",
              "value": False
            },
            {
              "name": "MULTI_SELECT",
              "value": False
            }
          ],
          "id": "f866f6020458477495d09f28a7680012",
          "optionAttributes": [
            {
              "name": "OPTION",
              "options": [
                {
                  "id": "f0001",
                  "index": 0,
                  "value": "第一个选项"
                },
                {
                  "id": "f0002",
                  "index": 1,
                  "value": "第二个选项"
                },
                {
                  "id": "f0003",
                  "index": 2,
                  "value": "第三个选项"
                }
              ]
            }
          ],
          "stringAttributes": [
            {
              "name": "TITLE",
              "value": "优先级"
            }
          ],
          "type": "DROP_DOWN_BOX"
        },
        {
          "booleanAttributes": [
            {
              "name": "REQUIRED",
              "value": False
            },
            {
              "name": "MULTI_SELECT",
              "value": False
            }
          ],
          "id": "f866f6020458477495d09f28a7680013",
          "stringAttributes": [
            {
              "name": "TITLE",
              "value": "备注"
            },
            {
              "name": "PLACE_HOLDER",
              "value": "你当前的想法"
            }
          ],
          "type": "MULTI_LINE_TEXT"
        },
        {
          "booleanAttributes": [
            {
              "name": "REQUIRED",
              "value": False
            },
            {
              "name": "MULTI_SELECT",
              "value": True
            }
          ],
          "id": "f866f6020458477495d09f28a7680014",
          "stringAttributes": [
            {
              "name": "TITLE",
              "value": "项目组人员"
            },
            {
              "name": "PLACE_HOLDER",
              "value": "请选择人员"
            }
          ],
          "type": "PERSON"
        },
        {
          "booleanAttributes": [
            {
              "name": "REQUIRED",
              "value": True
            }
          ],
          "id": "f866f6020458477495d09f28a7680015",
          "stringAttributes": [
            {
              "name": "TITLE",
              "value": "出发日期"
            }
          ],
          "type": "DATE"
        },
        {
          "booleanAttributes": [
            {
              "name": "REQUIRED",
              "value": False
            }
          ],
          "id": "f866f6020458477495d09f28a7680016",
          "stringAttributes": [
            {
              "name": "TITLE",
              "value": "上传附件"
            }
          ],
          "type": "ATTACHMENT"
        },
        {
          "booleanAttributes": [
            {
              "name": "REQUIRED",
              "value": True
            }
          ],
          "id": "f866f6020458477495d09f28a7680017",
          "stringAttributes": [
            {
              "name": "TITLE",
              "value": "引用资料"
            }
          ],
          "type": "REF_DOC"
        },
        {
          "booleanAttributes": [
            {
              "name": "REQUIRED",
              "value": True
            }
          ],
          "id": "f866f6020458477495d09f28a7680018",
          "stringAttributes": [
            {
              "name": "TITLE",
              "value": "引用BIM"
            }
          ],
          "type": "REF_BIM"
        },
        {
          "booleanAttributes": [
            {
              "name": "REQUIRED",
              "value": False
            },
            {
              "name": "MULTI_SELECT",
              "value": False
            }
          ],
          "id": "f866f6020458477495d09f28a7680019",
          "refAttributes": [
            {
              "name": "REF_PROC_TMPL",
              "refType": "PROC_TMPL",
              "refs": []
            }
          ],
          "stringAttributes": [
            {
              "name": "TITLE",
              "value": "关联流程"
            }
          ],
          "type": "REF_PROC"
        }
      ]
    ],
    "id": None
  },
  "procTmpl": {
    "id": None,
    "processNodeList": [
      {
        "approvalType": 1,
        "approverRoleList": [],
        "approverType": 0,
        "approverUserList": [],
        "auths": [
          {
            "auth": 4,
            "componentId": "f866f6020458477495d09f28a7680011"
          },
          {
            "auth": 4,
            "componentId": "f866f6020458477495d09f28a7680012"
          },
          {
            "auth": 4,
            "componentId": "f866f6020458477495d09f28a7680013"
          },
          {
            "auth": 4,
            "componentId": "f866f6020458477495d09f28a7680014"
          },
          {
            "auth": 4,
            "componentId": "f866f6020458477495d09f28a7680015"
          },
          {
            "auth": 4,
            "componentId": "f866f6020458477495d09f28a7680016"
          },
          {
            "auth": 4,
            "componentId": "f866f6020458477495d09f28a7680017"
          },
          {
            "auth": 4,
            "componentId": "f866f6020458477495d09f28a7680018"
          },
          {
            "auth": 4,
            "componentId": "f866f6020458477495d09f28a7680019"
          }
        ],
        "nodeName": "发起人"
      },
      {
        "approvalType": 1,
        "approverRoleList": [
          {
            "roleId":"f719d8e6507945549441050863f4070c"
          }
        ],
        "approverType": 0,
        "approverUserList": [],
        "auths": [
          {
            "auth": 2,
            "componentId": "f866f6020458477495d09f28a7680011"
          },
          {
            "auth": 2,
            "componentId": "f866f6020458477495d09f28a7680012"
          },
          {
            "auth": 2,
            "componentId": "f866f6020458477495d09f28a7680013"
          },
          {
            "auth": 2,
            "componentId": "f866f6020458477495d09f28a7680014"
          },
          {
            "auth": 2,
            "componentId": "f866f6020458477495d09f28a7680015"
          },
          {
            "auth": 2,
            "componentId": "f866f6020458477495d09f28a7680016"
          },
          {
            "auth": 2,
            "componentId": "f866f6020458477495d09f28a7680017"
          },
          {
            "auth": 2,
            "componentId": "f866f6020458477495d09f28a7680018"
          },
          {
            "auth": 2,
            "componentId": "f866f6020458477495d09f28a7680019"
          }
        ],
        "nodeName": "角色节点权限可读"
      },
      {
        "approvalType": 1,
        "approverRoleList": [],
        "approverType": 1,
        "approverUserList": [
          {"userName":"hubiao"},
          {"userName":"xialujie"},
          {"userName":"xushenwei"}
        ],
        "auths": [
          {
            "auth": 4,
            "componentId": "f866f6020458477495d09f28a7680011"
          },
          {
            "auth": 4,
            "componentId": "f866f6020458477495d09f28a7680012"
          },
          {
            "auth": 4,
            "componentId": "f866f6020458477495d09f28a7680013"
          },
          {
            "auth": 2,
            "componentId": "f866f6020458477495d09f28a7680014"
          },
          {
            "auth": 2,
            "componentId": "f866f6020458477495d09f28a7680015"
          },
          {
            "auth": 2,
            "componentId": "f866f6020458477495d09f28a7680016"
          },
          {
            "auth": 1,
            "componentId": "f866f6020458477495d09f28a7680017"
          },
          {
            "auth": 1,
            "componentId": "f866f6020458477495d09f28a7680018"
          },
          {
            "auth": 1,
            "componentId": "f866f6020458477495d09f28a7680019"
          }
        ],
        "nodeName": "人员节点权限可写、可读、隐藏"
      }
    ],
    "remark": "测试自定义流程类型模板编写的备注信息全控件",
    "sponsorRoleList": [],
    "sponsorType": 0,
    "sponsorUserList": [],
    "typeName": "测试Center发布成功，模板引擎发布失败BUGd"
  },
  "processFormAuthId": None
}
        response = CenterProcess.JsonRequest('post', resource, body)
        assert response["status_code"] == 200

    # def test_getproc_form_tmpl(self,CenterProcess):
    #     '''
    #     获取流程类型模板详情
    #     '''
    #     resource = f'/process/proc_form_tmpl/{procDefKey}'
    #     response = CenterProcess.JsonRequest('get',resource)
    #     assert response["status_code"] == 200

    # def test_template_switchStatus(self,CenterProcess):
    #     '''
    #     流程模板更新启用状态
    #     '''
    #     resource = f'/process/template/switchStatus/{procDefKey}'
    #     response = CenterProcess.JsonRequest('put',resource)
    #     assert response["status_code"] == 200

    def test_del_template(self,CenterProcess):
        '''
        批量删除流程模板
        '''
        resource = f'/process/template'
        body = ["X1574fc6c4464aa3a4b616004fe376c3"]
        response = CenterProcess.JsonRequest('delete',resource,body)
        assert response["status_code"] == 200

if __name__ == '__main__':
    pytest.main(["-s", "test_process.py"])