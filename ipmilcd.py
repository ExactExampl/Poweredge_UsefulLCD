from time import sleep
from subprocess import Popen
from sys import exit
from multiprocessing import cpu_count
import psutil, signal

translator = '/usr/sbin/ipmilcd/lcd'
threads_num = cpu_count()
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
    while not stopped:
        if threads_num == 24 or threads_num == 12: # 2 six-core cpu`s case
            t1 = psutil.sensors_temperatures()["coretemp"][0]
            t2 = psutil.sensors_temperatures()["coretemp"][1]
            t3 = psutil.sensors_temperatures()["coretemp"][2]
            t4 = psutil.sensors_temperatures()["coretemp"][3]
            t5 = psutil.sensors_temperatures()["coretemp"][4]
            t6 = psutil.sensors_temperatures()["coretemp"][5]
            t7 = psutil.sensors_temperatures()["coretemp"][6]
            t8 = psutil.sensors_temperatures()["coretemp"][7]
            t9 = psutil.sensors_temperatures()["coretemp"][8]
            t10 = psutil.sensors_temperatures()["coretemp"][9]
            t11 = psutil.sensors_temperatures()["coretemp"][10]
            t12 = psutil.sensors_temperatures()["coretemp"][11]
            
            tlist1 = [int(t1.current), int(t2.current), int(t3.current), 
                      int(t4.current), int(t5.current), int(t6.current)]
            approxtemp1 = int(sum(tlist1) / len(tlist1))
            
            tlist2 = [int(t7.current), int(t8.current), int(t9.current), 
                      int(t10.current), int(t11.current), int(t12.current)]
            approxtemp2 = int(sum(tlist2) / len(tlist2))
        
        elif threads_num == 8 or threads_num == 4: # 2 dual core cpu`s case`
            t1 = psutil.sensors_temperatures()["coretemp"][0]
            t2 = psutil.sensors_temperatures()["coretemp"][1]
            t3 = psutil.sensors_temperatures()["coretemp"][2]
            t4 = psutil.sensors_temperatures()["coretemp"][3]
            
            tlist1 = [int(t1.current), int(t2.current)]
            approxtemp1 = int(sum(tlist1) / len(tlist1))
            
            tlist2 = [int(t3.current), int(t4.current)]
            approxtemp2 = int(sum(tlist2) / len(tlist2))
            
        else: # else there is only two quad core cpu`s case left
            t1 = psutil.sensors_temperatures()["coretemp"][0]
            t2 = psutil.sensors_temperatures()["coretemp"][1]
            t3 = psutil.sensors_temperatures()["coretemp"][2]
            t4 = psutil.sensors_temperatures()["coretemp"][3]
            t5 = psutil.sensors_temperatures()["coretemp"][4]
            t6 = psutil.sensors_temperatures()["coretemp"][5]
            t7 = psutil.sensors_temperatures()["coretemp"][6]
            t8 = psutil.sensors_temperatures()["coretemp"][7]
            
            tlist1 = [int(t1.current), int(t2.current), int(t3.current),
                      int(t4.current)]
            approxtemp1 = int(sum(tlist1) / len(tlist1))
            
            tlist2 = [int(t5.current), int(t6.current), int(t7.current), 
                      int(t8.current)]
            approxtemp2 = int(sum(tlist2) / len(tlist2))
        return approxtemp1, approxtemp2
    
cptemp1, cptemp2 = cputemp()
    
while not stopped:
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