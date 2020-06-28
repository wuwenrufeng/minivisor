#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
@File: minivisor.py
@Project: minivisor
@Desc: 监控进程
@Time: 2020/06/28 16:51:06
@Author: wuwenrufeng (wuwenrufeng@163.com)
@Last Modified: 2020/06/28 16:51:06
@Modified By: wuwenrufeng (wuwenrufeng@163.com)
@Version: 1.0
@License: Copyright(C) 2019 - 2020 Borland
"""


import getopt
import os
import re
import signal
import subprocess
import sys
import time
from subprocess import check_output

import redis
import settings
import spider_conf
from scrapy import cmdline


def coursepid_kill(pid, delay):
    """
        根据进程id 删除该进程
    """
    try:
        time.sleep(delay)
        a = os.kill(pid, signal.SIGKILL)
        # a = os.kill(pid, signal.9) #　与上等效
        print('已杀死pid为%s的进程,　返回值是:%s' % (pid, a))
    except:
        pass

def coursepid(name):
    """
        根据进程名称，获得进程id
    """
    child = subprocess.Popen(['pgrep', '-f', name], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]
    return [int(pid) for pid in response.split()]

def list_all_files():
    redisdb = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PWD)
    # redisdb = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    for s in spider_conf.spider_list:
        count = 0
        # 查询该队列是否为空，如果不为空，则启动该进程，否则kill该进程
        for k in s['rediskeys']:
            if redisdb.llen(k):
                # 如果不为空，则结束该循环
                count = 1
                break

        pid = coursepid(s['name']) # 进程id
        if count:
            # 如果队列不为空，判断该spider 是否已经启动，如果启动，则不重复启动
            num = s['num']- len(pid) # 需要启动的进程数 和已存在的进程数
            if num:
                #print (num,type(num))
                i = 0
                for p in range(num):
                    i = i+1
                    # 启动进程
                    if "&" in s['scrapy']:
                        try:
                            os.system(s['scrapy'])
                        except:
                            pass
        else:
            #队列为空，需要删除该进程 
            for p in pid:
                coursepid_kill(p, s['delay'])
            

if __name__ == '__main__':
    list_all_files()
    pid = os.getpid()
    os.kill(pid,signal.SIGKILL)
