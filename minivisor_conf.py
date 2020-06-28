#_*_ coding:ut#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File: minivisor_conf.py
@Project: minivisor
@Desc: 配置文件
        根据队列名称启动对应的 spider 和个数
        {
            name spider的名称 (该名称用于队列为空的时候，杀死进程,所以该名称必须和启动的名称一样)
            cname spider的中文名称
            num 启动个数
            delay 杀死进程前的延时时间，针对用scrapy爬取响应慢的网站时，误杀最后一次请求
            rediskeys 对应的队列
            scrapy 启动的命名 *** 主要需要在 启动脚本后面加上 & 符号
        }
@Time: 2020/06/28 16:51:06
@Author: wuwenrufeng (wuwenrufeng@163.com)
@Last Modified: 2020/06/28 16:51:06
@Modified By: wuwenrufeng (wuwenrufeng@163.com)
@Version: 1.0
@License: Copyright(C) 2019 - 2020 Borland
"""

spider_list =[
                {
                    "cname": "百姓网整租列表页", 
                    "name": "[baixingwang]_zhengzu_list_crawl",
                    "num": 4, 
                    "delay": 1,
                    "rediskeys": ['baixingwang_zhengzu_list_queue'],
                    "scrapy": "scrapy crawl baixingwang_zhengzu_list_crawl -s PROXIES=proxies &"
                },

                {
                    "cname": "百姓网整租详情页", 
                    "name": "[baixingwang]_zhengzu_info_crawl",
                    "num": 4, 
                    "delay": 1,
                    "rediskeys": ['baixingwang_zhengzu_info_queue'],
                    "scrapy": "scrapy crawl baixingwang_zhengzu_info_crawl -s PROXIES=proxies &"
                },
] 
