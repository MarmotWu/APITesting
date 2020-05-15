#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @TIME    : 2018/7/31 17:34
# @Author  : hubiao
# @File    : Config.py
import configparser
import os


class ManageConfig:
    '''
    配置管理
    '''
    def __init__(self,filename='release.ini'):
        self.conf_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+os.sep+'Config'+os.sep+filename
        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("请确保配置文件存在！")
        self.config = configparser.RawConfigParser()

    def getConfig(self,section):
        '''
        获取指定节点下的配置
        :param section: 节点名称
        :return: 返回指定节点下的全部配置信息
        '''
        try:
            self.config.read(self.conf_path,encoding='utf-8-sig')
            return self.config[section]
        except BaseException as e:
            print("读取失败！", str(e))

    def getAllConfig(self):
        '''
        获取全部节点配置信息
        :return: 返回全部配置信息
        '''
        try:
            self.config.read(self.conf_path,encoding='utf-8-sig')
            return self.config
        except BaseException as e:
            print("读取失败！", str(e))

    def writeConfig(self,section,key,value):
        '''
        写入配置信息到指定的节点
        :param section: 节点名
        :param key: 配置的key信息
        :param value: 配置的value信息
        :return:
        '''
        try:
            #必须要先读取全部数据，再写入，不然数据会被覆盖
            self.config.read(self.conf_path,encoding='utf-8-sig')
            #判断节点是否存在，不存在时添加节点
            if self.config.has_section(section) is False:
                self.config[section] = {}
            self.config.set(section,key,value)
            with open(self.conf_path,'w',encoding='utf-8-sig') as configfile:
                self.config.write(configfile)
        except BaseException as e:
            print("写入失败！", str(e))

if __name__ == '__main__':
    #读取信息
    cf = ManageConfig()
    # rf = cf.getConfig('pds')
    # print(rf["pdsUrl"])
    #写入信息
    cf.writeConfig('pdsd','cdas','http://cas.com')

