#encoding=utf-8
'''
运行环境：python2.7
依赖：paramiko

'''
import paramiko

# 封装SSH类
class SSH(object):
    def __init__(self,host,user,port,pwd):
        self.ssh = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
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
        msg['stderr'] = stderrs
        return msg
    def ssh_close(self):
        self.ssh.close()


Test=SSH(host='172.16.161.2',user='root',port='22',pwd='!QAZ2wsx')

returm_msg = Test.cmd_run('ls')
print returm_msg['stdout']

Test.ssh_close()
