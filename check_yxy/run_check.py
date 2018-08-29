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
            'pwd':'111111',
            'port':'22',
        },
        'p23':{
            'host_ip':'p23',
            'user':'root',
            'pwd':'111111',
            'port':'22',
        },
        'p24':{
            'host_ip':'p24',
            'user':'root',
            'pwd':'111111',
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
}

mail_to_user=[
    'team_cloud_service@syberos.com',
]

#--------------------------------------------------------------------------------------
#以下为全局变量，请勿修改
global SEND_MAIB_BIT
SEND_MAIB_BIT=True

class SSH(object):
    '''
       封装SSH连接类，用于快速调用
    '''
    def __init__(self,host,user,port,pwd):
        self.Error_log=Error_Log()
        try:
            self.ssh = paramiko.SSHClient()
            # 允许连接不在know_hosts文件中的主机
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if pwd == '':
                #免密连接服务器
                key=paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
                self.ssh.connect(hostname=host, port=port, username=user, pkey=key, timeout=10)
            else:
                # 密码连接服务器
                self.ssh.connect(hostname=host, port=port, username=user, password=pwd, timeout=10)
        except Exception,e:
            global SEND_MAIB_BIT
            SEND_MAIB_BIT = False
            self.Error_log.error_save('ERROR:' + host + 'ssh 失败\n' )
            print 'ssh 失败'

    def cmd_run(self,cmd):
        '''
            运行命令获取返回值
        '''
        msg={
            'stdin':'',
            'stdout':'',
            'stderr':'',
        }
        try:
            print '---------------------------------------'
            stdin, stdout,stderr = self.ssh.exec_command(cmd,timeout=10)
            msg['stdin'] =stdin
            msg['stdout'] = stdout.read()
            msg['stderr'] = stderr
        except Exception,e:
            msg['stdout'] =' '
            global SEND_MAIB_BIT
            SEND_MAIB_BIT = False
            self.Error_log.error_save('ERROR:' + cmd + '运行 失败\n' )
            print '命令运行失败'
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
            os.system('echo `date` > CheckErrorSave.file')
    def error_save(self,msg):
        '''
            追加日志
        '''
        print msg
        os.system('echo "' + msg + '" >> CheckErrorSave.file')

#公共函数
def Send_mail(users):
    '''
        发送邮件
    '''
    global SEND_MAIB_BIT
    print SEND_MAIB_BIT
    if SEND_MAIB_BIT:
        for i in users:
            # print 'echo `date`  '
            os.system('echo `date` > sandrundata.file')
            os.system('echo "检测服务全部正常" >> sandrundata.file')
            os.system('mail -s "云服务检测正常`date`" '+i+' < ./sandrundata.file')
    else:
        for i in users:
            print 'mail -s "云服务出错`date`" '+i+' < ./CheckErrorSave.file'
            os.system('mail -s "云服务出错`date`" '+i+' < ./CheckErrorSave.file')

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
        print 'Server port'+ str(port) +'OK!'
    except Exception,e:
        print 'Server port'+ str(port) + 'not connect!'
    sk.close()

    return check_bit

def check_ping(host_ip):
    '''
        ping 主机测试
    '''
    check_bit=False
    remsg = os.system('ping -c 4 ' + host_ip +' > /dev/null' )
    if remsg:
        print host_ip+'ping bad'
        pass
    else:
        check_bit=True
        print host_ip+'ping ok'
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
            print 'master ok'
        else:
            check_bit=False
            global SEND_MAIB_BIT
            SEND_MAIB_BIT = False
            Error_log.error_save('ERROR:master'+host['host_ip'] + ' 节点数小于3 请及时查看\n' )
            print '节点数小于3'
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + 'maser ip 失联 无法ping通\n' )
        print '无法ping通'

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
            print '挂载ok'
        else:
            check_bit=False
            global SEND_MAIB_BIT
            SEND_MAIB_BIT = False
            Error_log.error_save('ERROR:' + host['host_ip'] + '挂载出错，请及时查看')
            print '挂载出错'
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' 失联 无法ping通\n' )
        print host['host_ip'] + ' 失联 无法ping通'

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
        print "registry is ok "
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' registry 仓库无法访问\n' )
        print 'registry is error'

    return check_bit

    # print http_msg.readlines()
    # print https_msg.readlines()

def check_docker(host):
    '''
        检测docker 服务状态
    '''
    Error_log=Error_Log()
    check_bit=False
    if check_ping(host_ip=host['host_ip']):
        ssh=SSH(host=host['host_ip'],user=host['user'],port=host['port'],pwd=host['pwd'])
        remsg=ssh.cmd_run('systemctl status docker | grep running | wc -l')
        print remsg['stdout']
        ssh.ssh_close()
        if int(remsg['stdout'])== 1:
            check_bit=True
            print 'docker ok'
        else:
            check_bit=False
            global SEND_MAIB_BIT
            SEND_MAIB_BIT = False
            Error_log.error_save('ERROR:' + host['host_ip'] + ' docker 运行出错\n' )
            print 'docker error'
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' 主机失联\n' )
        print '主机失联'
    return check_bit
        # print 'docker bad'

def check_DNS(host):
    '''
        检测DNS地址配置
    '''
    Error_log=Error_Log()
    check_bit=False
    if check_ping(host_ip=host['host_ip']):
        ssh=SSH(host=host['host_ip'],user=host['user'],port=host['port'],pwd=host['pwd'])
        remsg1=ssh.cmd_run("cat /etc/resolv.conf | grep 'search default.svc.syberyun.local svc.syberyun.local syberyun.local' | wc -l")
        remsg2=ssh.cmd_run("cat /etc/resolv.conf | grep 'nameserver 172.16.160.39' | wc -l")
        ssh.ssh_close()
        if int(remsg1['stdout'] ) == 1 and int(remsg2['stdout'] ) == 1:
            check_bit=True
            print 'DNS ok'
        else:
            check_bit=False
            global SEND_MAIB_BIT
            SEND_MAIB_BIT = False
            Error_log.error_save('ERROR:' + host['host_ip'] + ' DNS配置 运行出错\n' )
            print 'DNS配置 bad'
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' 主机失联\n' )
        print '主机失联'
    return check_bit

def check_Etcd(host):
    '''
        检测ETCD服务
    '''
    Error_log=Error_Log()
    check_bit=False
    if check_ping(host_ip=host['host_ip']):
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
            print 'etcd error'
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' 主机失联\n' )
        print '主机失联'
    return check_bit


def check_mysql(host):
    '''
        检测mysql服务
    '''
    Error_log=Error_Log()
    check_bit=False
    server_check_bit=False
    port_check_bit=False
    if check_ping(host_ip=host['host_ip']):
        if check_docker(host=host):
            server_check_bit=True
            print 'mysql ok'
        else:
            server_check_bit=False
            global SEND_MAIB_BIT
            SEND_MAIB_BIT = False
            Error_log.error_save('ERROR:' + host['host_ip'] + ' docker--mysqld 服务运行出错\n' )
            print ' mysqld 服务运行出错'

        # ssh=SSH(host=host['host_ip'],user=host['user'],port=host['port'],pwd=host['pwd'])
        # remsg=ssh.cmd_run('systemctl status mysqld | grep running | wc -l')
        # print remsg['stdout']
        # ssh.ssh_close()
        # if int(remsg['stdout'] ) == 1:
        #     server_check_bit=True
        #     print 'mysql ok'
        # else:
        #     server_check_bit=False
        #     global SEND_MAIB_BIT
        #     SEND_MAIB_BIT = False
        #     Error_log.error_save('ERROR:' + host['host_ip'] + ' mysqld 服务运行出错\n' )
        #     print ' mysqld 服务运行出错'
    else:
        server_check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' 主机失联\n' )
        print '主机失联'
    if check_port(host_ip=host['host_ip'],port=3306):
        port_check_bit=True
        print '3306端口连接 ok'
    else:
        port_check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' mysqld 3306端口无法连接\n' )
        print 'mysqld 3306端口无法连接'

    if server_check_bit and port_check_bit:
        check_bit=True
        print 'msyql ok'
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' mysqld 服务出错\n' )
        print 'msyql bad'
    return check_bit

def check_webserver(host):
    check_bit=False
    Error_log=Error_Log()
    if check_port(host_ip=host['host_ip'],port=8090):
        check_bit=True
        print 'webserver ok'
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + 'webserver 8090端口无法连接\n' )
        print 'webserver 8090端口无法连接'
    return check_bit

def check_gitlab(host):
    check_bit=False
    Error_log=Error_Log()
    if check_port(host_ip=host['host_ip'],port=80):
        check_bit=True
        print 'gitlab ok'
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + 'gitlab 80端口无法连接\n' )
        print 'gitlab 80端口无法连接'
    return check_bit

def check_jenkins(host):
    check_bit=False
    Error_log=Error_Log()
    if check_port(host_ip=host['host_ip'],port=8080):
        check_bit=True
        print 'jenkins ok'
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + 'jenkins 8080端口无法连接\n' )
        print 'jenkins 8080端口无法连接'
    return check_bit

def check_P25(host):
    '''
        为满足检测regis仓库的挂载，特别添加的检测函数
    '''
    check_bit=False
    Error_log=Error_Log()
    curl_check_bit=False
    mount_check_bit=False
    # if check_registry(host=host):
    if check_ping(host_ip=host['host_ip']):
        ssh=SSH(host=host['host_ip'],user=host['user'],port=host['port'],pwd=host['pwd'])
        remsg=ssh.cmd_run('df -hl | grep /dev/sdb1 | grep data | wc -l')
        ssh.ssh_close()
        if int(remsg['stdout'] ) == 1:
            mount_check_bit = True
            print '25 挂载ok'
        else:
            mount_check_bit=False
            global SEND_MAIB_BIT
            SEND_MAIB_BIT = False
            Error_log.error_save('ERROR:' + host['host_ip'] + '挂载出错，请及时查看')
            print '25 挂载出错'
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' 失联 无法ping通\n' )
        print '失联 无法ping通'
    if check_registry(host=host):
        curl_check_bit=True
    else:
        curl_check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' registry curl 检测异常\n' )
        print 'registry curl 检测异常'
    if curl_check_bit and mount_check_bit:
        check_bit=True
        print 'registry 检测为正常'
    else:
        check_bit=False
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        Error_log.error_save('ERROR:' + host['host_ip'] + ' registry 检测异常\n' )
        print 'registry curl 检测异常'


    return check_bit



#主函数
def check_all(host):
    '''
        主函数，配置具体检测项
    '''
    try:
        log=Error_Log()
        log.mk_log_file()
        check_master(host=host['master']['p1'])
        check_mount(host=host['node']['p180'])
        check_P25(host=host['registry']['p25'])
        check_docker(host=host['node']['p180'])
        check_docker(host=host['node']['p181'])
        check_docker(host=host['node']['p182'])
        check_Etcd(host=host['etcds']['p22'])
        check_Etcd(host=host['etcds']['p23'])
        check_Etcd(host=host['etcds']['p24'])
        check_mysql(host=host['yxy_mysql']['p4'])
        check_webserver(host=host['yxy_webserver']['p5'])
        check_gitlab(host=host['gitlab']['p8'])
        check_jenkins(host=host['jenkins']['p9'])
        Send_mail(users=mail_to_user)
    except Exception,e:
        print e
        global SEND_MAIB_BIT
        SEND_MAIB_BIT = False
        log.error_save('程序异常退出，请检测脚本运行状况')
        Send_mail(users=mail_to_user)



check_all(host=host)

