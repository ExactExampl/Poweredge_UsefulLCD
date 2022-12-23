from time import sleep
from subprocess import Popen
from sys import exit
import psutil, signal

translator = '/usr/sbin/ipmilcd/lcd'
threads_num = psutil.cpu_count(logical=False)
stopped = False
servname = 'change me' # Server name (must be 14 characters long)

def handle_stop(sig, frame):
    global stopped
    stopped = True
    Popen([translator, 'Nap time !'])
    sleep(1)
    Popen([translator, servname]) # Print server name
    sleep(.5)
    exit(0)

signal.signal(signal.SIGTERM, handle_stop)
signal.signal(signal.SIGHUP, handle_stop)
signal.signal(signal.SIGINT, handle_stop)

def cputemp():
    tsum1 = 0
    tsum2 = 0
    
    for n in range (threads_num // 2):
        t1 = psutil.sensors_temperatures()["coretemp"][n] 
        tsum1 += int(t1.current)
        approxtemp1 = tsum1 // (threads_num // 2)
    
    for x in range (threads_num // 2, threads_num):
        t2 = psutil.sensors_temperatures()["coretemp"][x] 
        tsum2 += int(t2.current)
        approxtemp2 = tsum2 // (threads_num // 2)
        
    return approxtemp1, approxtemp2
    
while not stopped:
    cptemp1, cptemp2 = cputemp()
    cputil = str(psutil.cpu_percent(0))
    Popen([translator, 'CPU:', cputil, '%'])
    sleep(3)
    ramutil = str(psutil.virtual_memory()[2])
    Popen([translator, 'RAM:', ramutil, '%'])
    sleep(3)
    Popen([translator, 'CPU1 t:', str(cptemp1),'`C'])
    sleep(3)
    Popen([translator, 'CPU2 t:', str(cptemp2),'`C'])
    sleep(3)
    Popen([translator, servname]) # Print server name
    sleep(3)