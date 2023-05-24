from time import sleep
from subprocess import Popen, check_output
from sys import exit
import psutil, signal

translator = '/usr/sbin/ipmilcd/lcd'
cpu_num = psutil.cpu_count(logical=False)
cpu_sockets = int(check_output('cat /proc/cpuinfo | grep "physical id" | sort -u | wc -l', shell=True))
stopped = False
servname = 'change me' # Server name (must be >= 14 chars)

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
    if cpu_sockets == 2: # We have regular dual socket setup
        for n in range (cpu_num // 2):
            t1 = psutil.sensors_temperatures()["coretemp"][n] 
            tsum1 += int(t1.current)
            approxtemp1 = tsum1 // (cpu_num // 2)
            
        for x in range (cpu_num // 2, cpu_num):
            t2 = psutil.sensors_temperatures()["coretemp"][x] 
            tsum2 += int(t2.current)
            approxtemp2 = tsum2 // (cpu_num // 2)
            
        return approxtemp1, approxtemp2
    else:  # We likely have a single cpu
        for n in range (cpu_num):
            t1 = psutil.sensors_temperatures()["coretemp"][n] 
            tsum1 += int(t1.current)
            approxtemp1 = tsum1 // cpu_num
            
        return approxtemp1
    
while not stopped:
    cputil = str(psutil.cpu_percent(0))
    Popen([translator, 'CPU:', cputil, '%'])
    sleep(3)
    ramutil = str(psutil.virtual_memory()[2])
    Popen([translator, 'RAM:', ramutil, '%'])
    sleep(3)
    if cpu_sockets == 2: # Dual cpu
        cptemp1, cptemp2 = cputemp()
        Popen([translator, 'CPU1 t:', str(cptemp1),'`C'])
        sleep(3)
        Popen([translator, 'CPU2 t:', str(cptemp2),'`C'])
    else: # Single cpu
        cputemp1 = cputemp
        Popen([translator, 'CPU t:', str(cptemp1),'`C'])
    sleep(3)
    Popen([translator, servname]) # Print server name
    sleep(3)