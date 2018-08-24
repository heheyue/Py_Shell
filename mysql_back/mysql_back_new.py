#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import time


#172.16.161.111@backup@cmccadmin!@syberos_db@/data/oa/syberos_db/@

# FILEPASH='/root/workspace/mysql_back/mysql_back/mysql_users/mysql_users_file.txt'
# ERRORLOG='/root/workspace/mysql_back/mysql_back/mysql_back_error.log'
# RUNLOG='/root/workspace/mysql_back/mysql_back/mysql_run.log'
# back=mysql_back(FILEPASH,ERRORLOG,RUNLOG)
# file_content = back.open_mysql_file()
# back.mysql_dump(file_content)
db_file_save_path = '/home/'
db_user_path = './config.d/'


class dbconf(object):
    def __init__(self):
        pass
    def get_db_info(self):
        pass

class config(object):
    #开关，标记是否使用扩展文件方式
    DB_DIR_BIT = True
    pass
class mysql_back(object):
    def __init__(self):
        pass
    def mysqldump(self,host_ip,user,passwd,db_name,db_save_path):
        pass
class public(object):
    def __init__(self):
        pass
    def return_now_time(self):
        pass