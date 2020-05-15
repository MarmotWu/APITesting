#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/3/22 17:57
# @Author  : hubiao
# @File    : run.py
"""
运行用例集：
    python3 run.py
# '--allure_severities=critical, blocker'
# '--allure_stories=测试模块_demo1, 测试模块_demo2'
# '--allure_features=测试features'
"""
import os,sys
import pytest
from Common import Log
from Common import Base

if __name__ == '__main__':
    print(len(sys.argv))
    if len(sys.argv)!=2:
        print ('Usage:python run.py case_catalogue allure-features intranet.ini')
        exit(0)
    print(sys.argv[0])
    print(sys.argv[1])
    print(sys.argv[2])
    print(sys.argv[3])
    if len(sys.argv)==3:
        allure_features = sys.argv[2]
    case_catalogue = sys.argv[1]
    log = Log.MyLog()
    report_path = case_catalogue+'/Report'
    report_path_html = report_path+'/html'
    print(report_path_html)

    # try:
    #     # 定义测试集
    #     allure_list = '--allure-features=全产品登录检查'
    #     py_args = ['TestCase\Polling\ExtractProjPolling','-s', '-q', '--alluredir',report_path,allure_list]
    #     log.info(f'执行用例集为：{allure_list}')
    #     pytest.main(py_args)
    #     # Base.shell(f'pytest -s -q --alluredir {xml_report_path} {allure_list}')
    # except Exception:
    #     log.error('执行用例失败，请检查环境配置')
    #     raise
    # try:
    #     log.info('开始生成allure报告')
    #     cmd = f'allure generate {report_path} -o {report_path_html} --clean'
    #     Base.shell(cmd)
    # except Exception:
    #     log.error('生成allure报告失败，请检查环境配置')
    #     raise
    # try:
    #     log.info('开始发送报告')
    # except Exception:
    #     log.error('发送报失败，请检查环境配置')
    #     raise