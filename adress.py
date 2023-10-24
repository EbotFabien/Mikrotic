import routeros_api
'''import os
hostname = "192.168.1.177" #example
response = os.system("ping " + hostname)
print(response)'''
import paramiko

IP='192.168.1.177'
'''connection = routeros_api.RouterOsApiPool(IP, username='fabien', password='fabien')
api = connection.get_api()
'''
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=IP, username='fabien', password='fabien')

stdin,stdout,stderr=ssh.exec_command(' /system routerboard print')
print(stdout.readlines())
'''stdin, stdout, stderr = ssh.exec_command('show run')

version_output = stdout.read()

print(version_output)'''
