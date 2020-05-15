#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/2/19 11:28
# @Author  : hubiao
# @File    : conftest.py
import pytest
from Common import HttpMethod
from Common import PublicLogin
from Common.Config import ManageConfig

@pytest.fixture(scope="session")
def BimAadminLogin():
    '''
    BIM Aadmin运维管理系统登录
    :return:
    '''
    section = 'sysadmin'
    BimAadminLogin = PublicLogin.BimAdmin(section=section).Login()
    yield BimAadminLogin

@pytest.fixture(scope="session")
def CenterCAS():
    '''
    获取Center CAS登录凭证
    :return:
    '''
    section = 'demoEnterprise'
    rf = ManageConfig().getConfig(section)
    PublicLogin.Center(rf["centerusername"], rf["centerpassword"],section).Login()
    yield

@pytest.fixture(scope="session")
def CenterBuilder(CenterCAS):
    '''
    获取Builder登录凭证
    :return:
    '''
    section = 'demoEnterprise'
    rf = ManageConfig().getConfig(section)
    CenterBuilder = HttpMethod.sendRequest(rf['builder'],section=section)
    yield CenterBuilder

@pytest.fixture(scope="session")
def PDSCAS():
    '''
    获取PDS登录凭证
    :return:
    '''
    section = 'sysadmin'
    rf = ManageConfig().getConfig(section)
    username = rf['newusername']
    password = "96e79218965eb72c92a549dd5a330112"
    PublicLogin.BV(username, password,section='mylubanapp').Login()
    yield

@pytest.fixture(scope="session")
def LBBV(PDSCAS):
    '''
    获取LBBV登录凭证
    :return:
    '''
    section = 'mylubanapp'
    rf = ManageConfig().getConfig(section)
    LBBV = HttpMethod.sendRequest(rf['lbbv'],section=section)
    yield LBBV

@pytest.fixture(scope="session")
def BimCO(PDSCAS):
    '''
    获取BimCO登录凭证
    :return:
    '''
    section = 'mylubanapp'
    rf = ManageConfig().getConfig(section)
    BimCO = HttpMethod.sendRequest(rf['bimco'],section=section)
    yield BimCO

@pytest.fixture(scope="session")
def Process(PDSCAS):
    '''
    获取Process登录凭证
    :return:
    '''
    section = 'mylubanapp'
    rf = ManageConfig().getConfig(section)
    Process = HttpMethod.sendRequest(rf['lbprocess'],section=section)
    yield Process