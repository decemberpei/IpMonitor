## IpMonitor - Daemon process to detect WAN Ip changes.
- My home network has a WAN Ip address assigned, but it's not a fixed one. Sometimes the Ip changes silently. To be able to connect to my home computer remotely 7x24, I have to know the new Ip once it changes.
- This Script check for WAN Ip peridically (once an hour), and reports(echo) the new Ip address to my VPS automatically.

### Set up steps:
- python3.8.10
- pip install requests paramiko
- Create new task for this script with "Windows Task Scheduler" and make it auto run at OS boot time. 
- The example command line to run this script is: 
	C:\Programs\Python36\pythonw.exe C:\Programs\IpMonitor\IpMonitor.py
- Check for log file IpMonitor.py.txt located beside IpMonitor.py to see how things are going.
