from requests import get
import time
import os
from datetime import datetime
import re
import paramiko
import socket

# change to your own VPS info
vps_ip = 'xx.xx.xx.xx'
vps_key = 'xx.pem'
vps_user = 'xx'

def get_wan_ip():
	p = {"http": "","https": "",}
	try:
		ip = get('https://api.ipify.org',proxies=p).content.decode('utf8')
		if ip is None:
			return None
		match = re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip)
		if match is None:
			log("Illegal Ip format: " + ip)
			return None
		return ip
	except Exception as e:
		log("Exception in get_wan_ip: " + str(e))
		return None

def safe_sleep(s):
	try:
		time.sleep(s)
	except Exception as e:
		pass

def log(content):
	print(content)
	try:
		timestamp = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
		log_file = open(__file__ + ".txt", "a")
		log_file.write(timestamp + " " + content + "\n" )
		log_file.close()
	except Exception as e:
		print("Log write error, ignore.")

def report_new_ip(ip):
	# global vps_ip, vps_key, vsp_user
	try:
		ssh = paramiko.SSHClient()
		k = paramiko.RSAKey.from_private_key_file(vps_key)
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(hostname=vps_ip, username=vps_user, pkey=k)
		stdin, stdout, stderr = ssh.exec_command('echo ' + ip + ' >> ' + socket.gethostname())
		out = stdout.read().decode()
		if len(out) > 0:
			log('cmd out:' + out)
		err = stderr.read().decode()
		if len(err) > 0:
			log('cmd err:' + out)
		ssh.close()
	except Exception as e:
		log("Exception in report_new_ip: " + str(e))

if __name__ == '__main__':
	log("Ip monitor starting.")
	init_ip = None
	now_ip = None

	init_ip = get_wan_ip()
	while init_ip is None:
		log("Fail to get Init Ip, sleep and retry.")
		safe_sleep(60)
		init_ip = get_wan_ip()
	log("Init Ip: " + init_ip)
	report_new_ip(init_ip)
	
	while True:
		time.sleep(3600)
		now_ip = get_wan_ip()
		while now_ip is None:
			log("Fail to get Ip, sleep and retry.")
			safe_sleep(60)
			now_ip = get_wan_ip()
		log("Now Ip: " + now_ip)
		if now_ip != init_ip:
			log("WAN Ip has changed, report new Ip.")
			report_new_ip(init_ip)
		else:
			log("Same Ip, continue monitor.")




