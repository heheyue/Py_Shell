#!/usr/bin/python
# -*- coding:utf-8 -*
import MySQLdb
import os

class mysql_user(object):
    def __init__(self):
        self.dbinfo = dict(host='127.0.0.1',user='root',passwd='',db='syberos_daq',charset="utf8") 
    def use_db(self,sql,params):
        #conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='syberos_daq')
        conn = MySQLdb.connect(**self.dbinfo)
        cur =conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)            
        cur.execute(sql,params)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
    
class syberos_daq(object):
    def __init__(self):
        self.__mysql=mysql_user()
    def select_id(self,username):
            sql="SELECT * FROM `daq_users` WHERE daq_name in ( %s )"
            in_p=', '.join(map(lambda x: '%s', username))
            sql= sql % in_p
            params=username
            return self.__mysql.use_db(sql,params)
class data_use(object):
    def re_daname_daqid_dict(self,grop,*data_dict):
        data_list=[]
        for i in data_dict: 
            for x in i:
                add_list={}
                #print x
                #print x.get('daq_name')
                #print x.get('id')
                add_list['username']=x.get('daq_name')
                add_list['userid']=x.get('id')
                add_list['displayname']=x.get('daq_username')
                add_list['grop']= grop
                data_list.append(add_list)
        return data_list
    def str_changeint(self,data):
        #print(data)
        list_now=[]
        for i in data:
            #print i
            for b in i:
                list_now.append(b)
        #print list_now
        #re_list=','.join(list_now)
        #print re_list
        return list_now
'''
# 数据库连接擦查询测试
username=[100431,200200]
db_test=syberos_daq()
db_re=db_test.select_id(username)
data=data_use()
now = data.re_daname_daqid_dict(db_re)
print now
'''   

class user_sys():
    def __init__(self,FILEPATH):           
        self.filepath = FILEPATH   
        
    def open_file(self):
        return_list=[]
        mysql_file=file(self.filepath,'r')
        for i in mysql_file.readlines():
            #print i
            #lines=i.strip('\n').split('\t')
            lines=i.strip('\n').split(' ')
            #print lines 
            return_list.append(lines)
        mysql_file.close()
        #print return_list
        return return_list
    def add_us(self,dict):
        #print dict
        for i in dict:
            #print i
            #return_info=os.popen("php ./JSR_user_interface.php %s %s %s %s;echo $?" % (i.get('username'),i.get('displayname'),i.get('userid'),i.get('grop')))
            print "php ./JSR_user_interface.php %s %s %s %s;echo $?" % (i.get('username'),i.get('displayname'),i.get('userid'),i.get('grop'))


txt="./user.txt"
grop='cmccadmi'
#处理文件内容
usefile=user_sys(txt)
db_test=syberos_daq()
data=data_use()
#打开文件并提取帐号
retu=usefile.open_file()
#print retu
#print retu
#改变字符
username=data.str_changeint(retu)
#print username
#查询用户数据
db_re=db_test.select_id(username)
#print db_re
#将查到的字典列表从新提取字段,返回
now = data.re_daname_daqid_dict(grop,db_re)
#print now
#添加用户
usefile.add_us(now)
