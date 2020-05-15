#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/3/20 16:46
# @Author  : hubiao
# @File    : conftest.py
import pytest
from Common import HttpMethod
from Common import PublicLogin
from Common.Config import ManageConfig

@pytest.fixture(scope="session")
def CenterCAS():
    '''
    获取Center CAS登录凭证
    :return:
    '''
    section = 'center'
    rf = ManageConfig().getConfig(section)
    PublicLogin.Center(rf["centerusername"], rf["centerpassword"],section=section).Login()
    yield

@pytest.fixture(scope="session")
def CenterBuilder(CenterCAS):
    '''
    获取Builder登录凭证
    :return:
    '''
    section = 'center'
    rf = ManageConfig().getConfig(section)
    CenterBuilder = HttpMethod.sendRequest(rf['builder'],section=section)
    yield CenterBuilder