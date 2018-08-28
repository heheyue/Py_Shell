#encoding=utf-8
'''
运行环境:python2.7
依赖:paramiko

'''
import os
import paramiko
import httplib
import socket
import time

#待检测机器配置
host={
    'master':{
        'p1':{
            'host_ip':'p1',
            'user':'root',
            'pwd':'',
            'port':'22',
        },
    },
    'node':{
        'p180':{
            'host_ip':'p180',
            'user':'root',
            'pwd':'',
            'port':'22',
        },
        'p181':{
            'host_ip':'p181',
            'user':'root',
            'pwd':'',
            'port':'22',
        },
        'p182':{
            'host_ip':'p182',
            'user':'root',
            'pwd':'',
            'port':'22',
        },
    },
    'etcds':{
        'p22':{
            'host_ip':'p22',
            'user':'root',
            'pwd':'',
            'port':'22',
        },
        'p23':{
            'host_ip':'p23',
            'user':'root',
            'pwd':'',
            'port':'22',
        },
        'p24':{
            'host_ip':'p24',
            'user':'root',
            'pwd':'',
            'port':'22',
        },
    },
    'registry':{
        'p25':{
            'host_ip':'p25',
            'user':'root',
            'pwd':'',
            'port':'22',
        }
    },
    'yxy_mysql':{
        'p4':{
            'host_ip':'p4',
            'user':'root',
            'pwd':'',
            'port':'22',
        }
    },
    'yxy_webserver':{
        'p5':{
            'host_ip':'p5',
            'user':'root',
            'pwd':'',
            'port':'22',
        }
    },
    'gitlab':{
        'p8':{
            'host_ip':'p8',
            'user':'root',
            'pwd':'',
            'port':'22',
        }
    },
    'jenkins':{
        'p9':{
            'host_ip':'p9',
            'user':'root',
            'pwd':'',
            'port':'22',
        }
    },
    'test':{
        'host_ip':'172.16.161.2',
        'user':'root',
        'pwd':'!QAZ2wsx',
        'port':'22',
    }

}

mail_to_user=[
    'yanxinyue@syberos.com',
]

#--------------------------------------------------------------------------------------
#以下为全局变量，请勿修改
global SEND_MAIB_BIT
SEND_MAIB_BIT=False

class SSH(object):
    '''
       封装SSH连接类，用于快速调用
    '''
    def __init__(self,host,user,port,pwd):
        self.ssh = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if pwd == '':
            #免密连接服务器
            self.ssh.connect(hostname=host, port=port, username=user, pkey=private_key)
        else:
            # 密码连接服务器
            self.ssh.connect(hostname=host, port=port, username=user, password=pwd)
    def cmd_run(self,cmd):
        '''
            运行命令获取返回值
        '''
        msg={
            'stdin':'',
            'stdout':'',
            'stderr':'',
        }
        stdin, stdout,stderr = self.ssh.exec_command(cmd)
        msg['stdin'] =stdin
        msg['stdout'] = stdout.read()
        msg['stderr'] = stderr
        return msg
    def ssh_close(self):
        '''
            关闭连接
        '''
        self.ssh.close()

class Error_Log(object):
    '''
        错误日志处理类
    '''
    def __init__(self):
        pass
    def mk_log_file(self):
        '''
            检测错误记录文件是否存在
                存在:删除创建
                不存在:直接创建
        '''
        if os.path.isfile("CheckErrorSave.file"):
            os.system('rm -rf CheckErrorSave.file')
            os.system('echo `date` > CheckErrorSave.file')
        else:
            os.system('echo `data` > CheckErrorSave.file')
    def error_save(self,msg):
        '''
            追加日志
        '''
        os.system('echo "' + msg + '" >> CheckErrorSave.file')

#公共函数
def Send_mail(msg):
    '''
        发送邮件
    '''
    global SEND_MAIB_BIT
    if SEND_MAIB_BIT:
        os.system('mail -s "云服务出错`date`" yanxinyue@syberos.com < ./CheckErrorSave.file')
    else:
        pass

def log_save():
    '''
        记录运行log
    '''
    pass



#公共项检测
def check_port(host_ip,port):
    '''
        检测端口是否开放
    '''
    check_bit=False
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(10)
    try:
        sk.connect((host_ip,int(port)))    #连接21号端口，并作出判断
        check_bit=True
        # print 'Server port 21 OK!'
    except Exception:
        pass
        # print 'Server port 21 not connect!'
    sk.close()

    return check_bit

def check_ping(host_ip):
    '''
        ping 主机测试
    '''
    check_bit=False
    remsg = os.system('ping -c 4 ' + host_ip +' > /dev/null' )
    if remsg:
        # print 'ping bad'
        pass
    else:
        check_bit=True
        # print 'ping ok'
    return check_bit


#详细项目检测函数
def check_master(host):
    '''
     #检测mster节点数量是否大于3
    '''
    # print host['master']['p1']
    Error_log=Error_Log()
    check_bit=False
    if check_ping(host_ip=host['host_ip']):
        ssh=SSH(host=host['host_ip'],user=host['user'],port=host['port'],pwd=host['pwd'])
        remsg=ssh.cmd_run('kubectl get node | wc -l ')
        # print remsg['stdout']
        ssh.ssh_close()
        if int(remsg['stdout'] ) >= 3:
            check_bit=True
            # print 'master ok'
        else:
            check_bit=False
            global SEND_MAIB_BIT
            SEND_MAIB_BIT = False
            Error_log.error_save('ERROR:master'+host['host_ip'] + ' 节点数小于3 请及时查看\n' )
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + 'maser ip 失联 无法ping通\n' )

    return check_bit

def check_mount(host):
    '''
        用于检测挂载状态---
        df -hl
        /dev/sda1       917G   43G  828G   5% /docker
        /dev/sda3       2.7T  4.2G  2.6T   1% /data
        /dev/sda2       1.8T  647M  1.7T   1% /mnt/data

    '''
    check_bit = False
    Error_log=Error_Log()
    if check_ping(host_ip=host['host_ip']):
        ssh=SSH(host=host['host_ip'],user=host['user'],port=host['port'],pwd=host['pwd'])
        remsg1=ssh.cmd_run('df -hl | grep /dev/sda1 | grep docker | wc -l')
        remsg2=ssh.cmd_run('df -hl | grep /dev/sda2 | grep data | wc -l')
        remsg3=ssh.cmd_run('df -hl | grep /dev/sda3 | grep data | wc -l')
        ssh.ssh_close()
        if int(remsg1['stdout'] ) == 1 and int(remsg2['stdout'] ) == 1 and int(remsg3['stdout'] ) == 1:
            check_bit = True
        else:
            check_bit=False
            global SEND_MAIB_BIT
            SEND_MAIB_BIT = False
            Error_log.error_save('ERROR:' + host['host_ip'] + '挂载出错，请及时查看')
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' 失联 无法ping通\n' )

    return check_bit

def check_registry(host):
    '''
        用于检测registry仓库是否正常
    '''
    Error_log=Error_Log()
    check_bit=False
    http_bit=False
    https_bit=False
    http_msg=os.popen('curl http://' + host['host_ip'] + ":5000/v2/_catalog | grep 'repositories' ")
    https_msg=os.popen('curl -k https://' + host['host_ip'] + ":5000/v2/_catalog  | grep 'repositories' ")
    for i in http_msg.readlines():
        if 'repositories' in i:
            http_bit=True
        else:
            pass
    for i in https_msg.readlines():
        if 'repositories' in i:
            https_bit=True
        else:
            pass
    if http_bit or https_bit:
        check_bit=True
        # print "registry is ok "
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' registry 仓库无法访问\n' )

    return check_bit

    # print http_msg.readlines()
    # print https_msg.readlines()

def check_docker(host):
    '''
        检测docker 服务状态
    '''
    Error_log=Error_Log()
    check_bit=False
    if check_ping(host=host['host_ip']):
        ssh=SSH(host=host['host_ip'],user=host['user'],port=host['port'],pwd=host['pwd'])
        remsg=ssh.cmd_run('systemctl status docker | grep running | wc -l')
        print remsg['stdout']
        ssh.ssh_close()
        if int(remsg['stdout'] ) == 1:
            check_bit=True
            print 'docker ok'
        else:
            check_bit=False
            global SEND_MAIB_BIT
            SEND_MAIB_BIT = False
            Error_log.error_save('ERROR:' + host['host_ip'] + ' docker 运行出错\n' )
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' 主机失联\n' )
    return check_bit
        # print 'docker bad'

def check_DNS(host):
    '''
        检测DNS地址配置
    '''
    Error_log=Error_Log()
    check_bit=False
    if check_ping(host=host['host_ip']):
        ssh=SSH(host=host['host_ip'],user=host['user'],port=host['port'],pwd=host['pwd'])
        remsg1=ssh.cmd_run("cat /etc/resolv.conf | grep 'search default.svc.syberyun.local svc.syberyun.local syberyun.local' | wc -l")
        remsg2=ssh.cmd_run("cat /etc/resolv.conf | grep 'nameserver 172.16.160.39' | wc -l")
        ssh.ssh_close()
        if int(remsg1['stdout'] ) == 1 and int(remsg2['stdout'] ) == 1:
            check_bit=True
            # print 'DNS ok'
        else:
            check_bit=False
            global SEND_MAIB_BIT
            SEND_MAIB_BIT = False
            Error_log.error_save('ERROR:' + host['host_ip'] + ' DNS配置 运行出错\n' )
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' 主机失联\n' )
    return check_bit

def check_Etcd(host):
    '''
        检测ETCD服务
    '''
    Error_log=Error_Log()
    check_bit=False
    if check_ping(host=host['host_ip']):
        ssh=SSH(host=host['host_ip'],user=host['user'],port=host['port'],pwd=host['pwd'])
        remsg=ssh.cmd_run('systemctl status etcd | grep running | wc -l')
        print remsg['stdout']
        ssh.ssh_close()
        if int(remsg['stdout'] ) == 1:
            check_bit=True
            print 'etcd ok'
        else:
            check_bit=False
            global SEND_MAIB_BIT
            SEND_MAIB_BIT = False
            Error_log.error_save('ERROR:' + host['host_ip'] + ' etcd 服务 运行出错\n' )
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' 主机失联\n' )
    return check_bit


def check_mysql(host):
    '''
        检测mysql服务
    '''
    Error_log=Error_Log()
    check_bit=False
    if check_ping(host=host['host_ip']):
        ssh=SSH(host=host['host_ip'],user=host['user'],port=host['port'],pwd=host['pwd'])
        remsg=ssh.cmd_run('systemctl status mysqld | grep running | wc -l')
        print remsg['stdout']
        ssh.ssh_close()
        if int(remsg['stdout'] ) == 1:
            check_bit=True
            print 'mysql ok'
        else:
            check_bit=False
            global SEND_MAIB_BIT
            SEND_MAIB_BIT = False
            Error_log.error_save('ERROR:' + host['host_ip'] + ' mysqld 服务运行出错\n' )
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' 主机失联\n' )
    if check_port(host=host['host_ip'],port=3306):
        check_bit=True
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' mysqld 3306端口无法连接\n' )
    return check_bit

def check_webserver(host):
    check_bit=False
    Error_log=Error_Log()
    if check_port(host['host_ip'],port=8090):
        check_bit=False
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + 'webserver 8090端口无法连接\n' )
    return check_bit

def check_gitlab(host):
    check_bit=False
    Error_log=Error_Log()
    if check_port(host['host_ip'],port=80):
        check_bit=False
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + 'gitlab 80端口无法连接\n' )
    return check_bit

def check_jenkins(host):
    check_bit=False
    Error_log=Error_Log()
    if check_port(host['host_ip'],port=8080):
        check_bit=False
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + 'jenkins 8080端口无法连接\n' )
    return check_bit


#主函数
def check_all(host):
    '''
        主函数，配置具体检测项
    '''
    log=Error_Log()
    log.mk_log_file()
    # check_master(host=host['test'])
    # check_mount(host=host['test'])
    check_registry(host=host['test'])



check_all(host=host)

