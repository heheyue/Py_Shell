#encoding=utf-8
'''
运行环境:python2.7
依赖:paramiko

'''
import os
import paramiko
import httplib

#待检测机器配置
host={
    'master':{
        'p1':{
            'host_ip':'172.16.160.174',
            'user':'root',
            'pwd':'!QAZ2wsx',
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
            'host_ip':'172.16.161.211',
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
        self.ssh.close()


def check_master(host):
    '''
     #检测mster节点数量是否大于3
    '''
    # print host['master']['p1']
    ssh=SSH(host=host['host_ip'],user=host['user'],port=host['port'],pwd=host['pwd'])
    remsg=ssh.cmd_run('kubectl get node | wc -l ')
    print remsg['stdout']
    ssh.ssh_close()
    if int(remsg['stdout'] ) >= 3:
        print 'master ok'
    else:
        print 'master bad'

def check_mount(host):
    '''
        用于检测挂载状态---
        df -hl
        /dev/sda1       917G   43G  828G   5% /docker
        /dev/sda3       2.7T  4.2G  2.6T   1% /data
        /dev/sda2       1.8T  647M  1.7T   1% /mnt/data

    '''
    check_bit = False
    ssh=SSH(host=host['host_ip'],user=host['user'],port=host['port'],pwd=host['pwd'])
    remsg1=ssh.cmd_run('df -hl | grep /dev/sda1 | grep docker | wc -l')
    remsg2=ssh.cmd_run('df -hl | grep /dev/sda2 | grep data | wc -l')
    remsg3=ssh.cmd_run('df -hl | grep /dev/sda3 | grep data | wc -l')
    if int(remsg1['stdout'] ) == 1 and int(remsg2['stdout'] ) == 1 and int(remsg3['stdout'] ) == 1:
        check_bit = True
    else:
        print 'mount bad'


def check_registry(host):
    '''
        用于检测registry仓库是否正常
    '''
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
        print "registry is ok "
    else:
        print "registry is bad"

    # print http_msg.readlines()
    # print https_msg.readlines()

def check_docker(host):
    pass
def check_DNS(host):
    pass
def check_Etcd(host):
    pass
def check_mysql(host):
    pass
def check_webserver(host):
    pass
def check_gitlab(host):
    pass
def check_jenkins(host):
    pass
# check_master(host=host['master']['p1'])
# check_mount()
# check_registry(host=host['registry']['p25'])

