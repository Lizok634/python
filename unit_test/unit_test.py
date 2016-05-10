# !/usr/bin/env python
# ^_^ coding=utf-8 ^_^!

# > File Name: unit_test.py
# > Author: louie.long
# > Mail: louie.long@pica8.local
# > Created Time: Tuesday, May 03, 2016 PM02:04:11 HKT


'''
This is a kernel sysfs unit test script
'''

import os
import os.path
import datetime

log_file = 'check_log'
config_file = 'config'

#init log file
def init_log():
    try:
        log = open(log_file, 'w')
        log.truncate()      #empty log file
        tmp = os.popen('version')   #get box name
        boxinfo = tmp.readlines();tmp.close()
        box = boxinfo[2].split(':')[1].strip()
        box = ''.join(['Box:', box])
        version = boxinfo[3].split(':')[1].strip()  #get system version
        version = ''.join(['version', ':', version])
        ip = os.popen('ifconfig | grep 10.10.51.')  #get box ip address
        addr = ip.read();ip.close();addr = addr.split(' ')
        ip = ''.join([x for x in addr if 'addr' in x])
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time = ''.join(['time:', time])   #get current time
        info = ''.join(['# ', box, '  ', version, '  ', ip, '  ', time])
        write_log(info)
        write_log('')
    except IOError:
        print "open log file failed"
        os._exit(-1)
    return

#write log file
def write_log(info, num = -1):
    try:
        log = open(log_file, 'a')
        if num == 0:        #sysfs path is not exist
            log.write("[failed]" + info + " is not exist"  + "\n")
            print ("[failed] " + info + " is not exist")
        if num == 1:        #open file success, and record file content
            log.write("[pass]" + info + "\n")
            print ("[pass] " + info)
        if num == 2:        #open file failed, or empty file
            log.write("[failed]" + info + "\n")
            print ("[failed] " + info)
        if num == -1:       #print check unit name
            log.write(info + "\n")
            print info
    except IOError:
        print "open log file failed"
        os._exit(-1)
    return log

#path check
def path_check(path_name, log):
    if os.path.exists(path_name) == False:
        print "%s is not exist" %path_name
        log.write(path_name + "is not exit" + '\n')
        log.close()
        os._exit(-1)
    return

#check info
def read_info(file_path):
    file_name = os.path.basename(file_path)
    try:
        f = open(file_path, 'r')
        value = f.readline().splitlines()
        tmp = ''.join(value)
        tmp = ''.join([file_name,'=',tmp])
        return tmp, 1, value
    except IOError:
        #tmp = ''.join([file_name, ' open failed'])
        return file_name, 2

#path_name_test = '/sys/class/hwmon/hwmon0'

#split config file
def config_split():
    with open(config_file, 'r') as f:
        config_tab = f.readlines()
        check_list = []
        arr = []
        for i,tmp in enumerate(config_tab):
            if tmp == '\n':
                arr.append(i)
        if len(config_tab)-1 not in arr:
            arr.append(len(config_tab)-1)
        for i,tmp in enumerate(arr):
            if tmp == arr[-1]:
                continue
            else:
                a=config_tab[arr[i] + 1 : arr[i+1]]
                check_list.append(a)
    return  check_list              


def check_config(check_list):
    for sys_path in check_list:
        if 'hwinfo' in sys_path[0]:
            check_hwinfo(sys_path)
            continue
        if 'psu' in sys_path[0]:
            check_psu(sys_path)
            continue
        if 'port' in sys_path[0]:
            check_ports(sys_path)
            continue
        if 'ctrl' in sys_path[0]:
            check_ctrl(sys_path)
            continue
        if 'leds' in sys_path[0]:
            check_leds(sys_path)
            contine
        if 'watchdog' in sys_path[0]:
            check_watchdog(sys_path)
            continue
    return

#check hwinfo 
def check_hwinfo(check_list):
    unit_name = check_list[0].strip()
    write_log(unit_name)
    dir_path = check_list[1].strip()
    if os.path.exists(dir_path) == False:
        write_log(dir_path, 0)
        write_log('')
        return
    for attr in check_list[2:]:
        attr = attr.strip()
        file_path = os.path.join(dir_path, attr)
        info = read_info(file_path)
        write_log(info[0], info[1])
    write_log('')
    return

#check psu
def check_psu(check_list):
    unit_name = check_list[0].strip()   #print unit test name
    write_log(unit_name)
    dir_path = check_list[1].strip()    #get unit test path
    if os.path.exists(dir_path) == False:   #check path exist or not
        write_log(dir_path, 0)
        write_log('')
        return
    psu_num = os.listdir(ditpath)
    for psu in psu_num:
        X = psu.replace('psu', '')  #get psu num
        psu_path = os.path.join(dir_path, psu_num)  #
        for attr in check_list[2:]:
            attr = attr.strip()
            if 'X' in attr:
                attr = attr.replace('X',X)
            file_path = os.path.join(dir_path, attr)
            info = read_info(file_path)
            if attr == 'present' and info[2] == '0':
                info[0] == psu.join(' is not present')    
                write_log(info[0])
            else:
                write_log(info[0], info[1])
    write_log('')
    return

#check ports
def check_ports(check_list):
    return


#check ctrl
def check_ctrl(check_list):
    return

#check watchdog
def check_watchdog(check_list):
    unit_name = check_list[0].strip()   #print unit test name
    write_log(unit_name)
    dir_path = check_list[1].strip()    #get unit test path
    if os.path.exists(dir_path) == False:   #check path exist or not
        write_log(dir_path, 0)
        write_log('')
        return
    attr = check_list[2].strip()
    file_path = os.path.join(dir_path, attr)
    info = read_info(file_path)
    if info[2] == '1':
        info[0] == psu.join(' enable')    
        write_log(info[0])
    elif info[2] == '0':
        info[0] == psu.join(' disable')
        write_log(info[0], 2)
    else:
        write_log(info[0], info[1])
    write_log('')
    return












if __name__=="__main__":
    init_log()
    #check_list = config_split()
    #check_config(check_list)


