#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
    用于数据库的备份
    建立数据库链接文件：
    格式：
            IP@user@passwd@name_from_db@fiel_back_path
            IP地址@用户名@数据库密码@库名@数据库备份文件地址
        192.168.130.11@root@cmccadmin!@app@/data/store/app@
'''
Array = {
 'YuanXin':{
     'test':{
         '172.16.160.107':{
             'syberos_db':{
                 'user':'root',
                 'password':'test'
             }
         }
     }
 }

}






class mysqldump_error(Exception):
    '''
    #自定义异常处理,未启用
    '''
    def __init__(self,num,info):
        self.num=num
        self.info=info
    def print_error(self):
        print "error is ok"     
        

class mysql_back(object):
    '''
         数据库备份类
         需要一个参数，为数据库连接文件
    '''
    def __init__(self,FILEPATH,ERRORFILE,RUNLOG):
        '''初始化函数
        '''
        self.filepath = FILEPATH
        self.errorfile = ERRORFILE
        self.runlog = RUNLOG
        
    def use_time(self):
        '''
             格式化时间
    '''
        import time
        return time.strftime('%Y%m%d-%H%M%S')
    
    def open_mysql_file(self):
        '''
                    从文件读取，并将其变为列表反回。
                    接收的文件如下格式：
            172.16.161.111@backup@cmccadmin!@syberos_db@/data/oa/syberos_db/@
                    每个字段以‘@’分割
                    变成组合列表返回
        '''
        return_list=[]
        mysql_file=file(self.filepath,'r')
        for i in mysql_file.readlines():
            #    print i
            lines=i.strip('\n').split('@')
            #    print lines 
            return_list.append(lines)
        mysql_file.close()
            #print return_list
        return return_list

    def mysql_dump(self,*arg):
        '''
            接收列表行参数。
        运行数据库备份命令，备份数据库。
        '''
        import os
        now_time=self.use_time()
        for i in  arg:
            for b in i:
                #sql_use="mysqldump -h%s -u%s -p%s --opt -R %s > %s/%s_%s.sql" % (b[0],b[1],b[2],b[3],b[4],b[3],now_time)
                #print sql_use
                #try:
                    return_info=os.popen("mysqldump -h%s -u%s -p%s --opt -R %s > %s/%s_%s.sql;echo $?" % (b[0],b[1],b[2],b[3],b[4],b[3],now_time))
                    mysql_info= return_info.read()
                    #print mysql_info
                    if int(mysql_info) == 0 :
                        pass
                        #print "ok"
                    else:
                        #print "%s : %s back is error >> ./mysql_back_error.log" % (now_time,b[0])
                        os.popen("echo %s:%s---%s--- back is error >> %s" % (now_time,b[0],b[3],self.errorfile))
                        #print 'error'
                        #raise mysqldump_error()
                #except:
                #        pass
        os.popen("echo ------------time:%s---mysql_back---end---------------- >> %s" % (now_time,self.runlog)) 
                    





FILEPASH='/root/workspace/mysql_back/mysql_back/mysql_users/mysql_users_file.txt'
ERRORLOG='/root/workspace/mysql_back/mysql_back/mysql_back_error.log'
RUNLOG='/root/workspace/mysql_back/mysql_back/mysql_run.log'                   
back=mysql_back(FILEPASH,ERRORLOG,RUNLOG)
file_content = back.open_mysql_file()
back.mysql_dump(file_content)