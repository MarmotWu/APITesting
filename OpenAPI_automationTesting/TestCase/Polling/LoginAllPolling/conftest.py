#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/2/19 11:28
# @Author  : hubiao
# @File    : conftest.py
import pytest
from Common import HttpMethod
from Common import PublicLogin
from Common.Config import ManageConfig

cf = ManageConfig()
pds = cf.getConfig('pds')

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
def BimAppLogin():
    '''
    BIMApp 通行证系统登录
    :return:
    '''
    section = 'bimapp'
    rf = ManageConfig().getConfig(section)
    username = rf['username']
    password = rf['password']
    BimAppLogin = PublicLogin.Bimapp(username,password,section=section).Login()
    yield BimAppLogin

@pytest.fixture(scope="session")
def MylubanWebLogin():
    '''
    Myluban web 登录
    :return:
    '''
    section = 'MylubanWeb'
    rf = ManageConfig().getConfig(section)
    username = rf['username']
    password = rf['password']
    MylubanWebLogin = PublicLogin.MylubanWeb(username,password,section=section).Login()
    yield MylubanWebLogin

@pytest.fixture(scope="session")
def BussinessLogin():
    '''
    Bussiness 业务管理系统登录
    :return:
    '''
    section = 'Bussiness'
    rf = ManageConfig().getConfig(section)
    username = rf['username']
    password = rf['password']
    BussinessLogin = PublicLogin.Bussiness(username,password).Login()
    yield BussinessLogin