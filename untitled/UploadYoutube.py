# -*- coding: utf-8 -*-
import paramiko
import datetime
import os
import configparser
import codecs

hostname = ""
port = 22
username = ""
password = ""
REMOTE_PATH = ""
LOCAL_PATH = ""

def loadConfig():
    global hostname
    global port
    global username
    global password
    global REMOTE_PATH

    f = codecs.open( "config.ini" , "r" ,encoding='UTF-8');
    config = configparser.ConfigParser()
    config.read_file(f)
    hostname = config.get("global","hostname")
    port = int(config.get("global","port"))
    username = config.get("global","username")
    password = config.get("global","password")
    REMOTE_PATH = config.get("global","REMOTE_PATH")

def upload(local_file, file):
    _localDir = LOCAL_PATH
    remote_file = REMOTE_PATH+file.replace('.mp4','.tmp')
    t = paramiko.Transport((hostname, port))
    try:

        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        print('start to upload video:'+local_file)
        sftp.put(local_file, remote_file)
        print('end upload video:'+remote_file)
        renameFile(remote_file)
    finally:
        t.close()


def renameFile(remote_file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, 22, username, password)
    ssh.exec_command("mv " + remote_file +' '+remote_file.replace('.tmp','.mp4'))
    ssh.close()


if __name__ == '__main__':
    loadConfig()
    upload('/home/willieyu/youtubeWork/6大嫁出國門又被老外“退貨”，狼狽回國撈金的明星.mp4',
           '6大嫁出國門又被老外“退貨”，狼狽回國撈金的明星.mp4')

# loadConfig()
# upload(LOCAL_PATH, REMOTE_PATH)
#
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(hostname, 22, username, password)
# stdin, stdout, stderr = ssh.exec_command("du -ah " + REMOTE_PATH)
# print (stdout.readlines())
# ssh.close()
