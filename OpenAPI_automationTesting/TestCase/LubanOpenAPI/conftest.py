#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2019/1/30 9:37
# @Author  : hubiao
# @File    : conftest.py

from Common.Config import ManageConfig
from Common import PublicLogin
from Common.Base import *
import pytest

@pytest.fixture(scope='session')
def OpenAPIToken():
    '''
    登录获取token
    '''
    section = 'openapi'
    rf = ManageConfig().getConfig(section)
    OpenAPIToken = PublicLogin.OpenAPI(rf['apikey'], getStrMD5(rf['apikey']),section).Login()
    yield OpenAPIToken


if __name__ == "__main__":
    OpenAPIToken()