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
        if num == -1:       #print info without prefix
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
        value = ''.join(value)
        tmp = ''.join([file_name,'=',value])
        f.close()
        return tmp, 1, value
    except IOError:
        #tmp = ''.join([file_name, ' open failed'])
        return file_name, 2, '0'

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
        if 'hwinfo' in sys_path[0]:     #hwinfo
            check_hwinfo(sys_path)
        elif 'psu' in sys_path[0]:      #psu
            check_psu(sys_path)
        elif 'sfp' in sys_path[0]:      #sfp
            check_sfp(sys_path)
        elif 'qsfp' in sys_path[0]:     #qsfp
            check_qsfp(sys_path)
        elif 'ctrl' in sys_path[0]:     #ctrl
            check_ctrl(sys_path)
        elif 'leds' in sys_path[0]:     #leds
            check_leds(sys_path)
        elif 'watchdog' in sys_path[0]: #watchdog
            check_watchdog(sys_path)
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
    psu_num = os.listdir(dir_path)
    for psu in psu_num:
        X = psu.replace('psu', '')  #get psu num
        psu_path = os.path.join(dir_path, psu)  #joint psu path
        tip = ''.join(['#********', psu, '********#'])
        write_log(tip)
        attrX = [''.join(x) for x in os.listdir(psu_path) if 'fan' in x or 'temp' in x]
        for x in sorted(attrX):
            check_list.append(x)

        for attr in check_list[2:]:
            attr = attr.strip()
            if 'X' in attr:
                continue
            file_path = os.path.join(psu_path, attr)
            info = read_info(file_path)
            if 'present' in attr and info[2] == '0':
                tmp = ''.join([psu, ' is not present'])    
                write_log(tmp)
                break
            else:
                write_log(info[0], info[1])
    write_log('')
    return

#check ports sfp
def check_sfp(check_list):
    unit_name = check_list[0].strip()   #print unit test name
    write_log(unit_name)
    dir_path = check_list[1].strip()    #get unit test path
    if os.path.exists(dir_path) == False:   #check path exist or not
        write_log(dir_path, 0)
        write_log('')
        return
    return

#check ports qsfp
def check_qsfp(check_list):
    return

#check ctrl
def check_ctrl(check_list):
    unit_name = check_list[0].strip()   #print unit test name
    write_log(unit_name)
    dir_path = check_list[1].strip()    #get unit test path
    if os.path.exists(dir_path) == False:   #check path exist or not
        write_log(dir_path, 0)
        write_log('')
        return

    fan_number = 0
    fanr_number = 0

    attr = check_list[2].strip()    #get fan number
    file_path = os.path.join(dir_path, attr)
    info = read_info(file_path)
    if info[2].isdigit() and int(info[2]) < 20:
        fan_number = info[2]
        attr = attr.join(['=',fan_number])
        write_log(attr, 1)
    else:
        write_log(attr, 2)
        exit(-1)

    attr = check_list[3].strip()    #get fanr number
    file_path = os.path.join(dir_path, attr)
    info = read_info(file_path)
    if info[2].isdigit() and int(info[2]) < 20:
        fanr_number = info[2]
        attr = attr.join(['=',fanr_number])
        write_log(attr, 1)
    else:
        write_log(attr, 2)
        exit(-1)

    for attr in check_list[4:]:
        attr = attr.strip()
        if 'fanX' in attr:  #get fanX info
            n = 1
            while n <= fan_number:
                attr = attr.replace('X',n)
                file_path = os.path.join(dir_path, attr)
                info = read_info(file_path)
                write_log(info[0], info[1])
                n += 1
        elif 'fanrX' in attr:   #get fanrX info
            n = 1
            while n <= fanr_number:
                attr = attr.replace('X',n)
                file_path = os.path.join(dir_path, attr)
                info = read_info(file_path)
                write_log(info[0], info[1])
                n += 1
        else:
            file_path = os.path.join(dir_path, attr)
            info = read_info(file_path)
            write_log(info[0], info[1])
    write_log('')
    return

#check leds
def check_leds(check_list):
    unit_name = check_list[0].strip()   #print unit test name
    write_log(unit_name)
    dir_path = check_list[1].strip()    #get unit test path
    if os.path.exists(dir_path) == False:   #check path exist or not
        write_log(dir_path, 0)
        write_log('')
        return
    attrX = [''.join([x, '/brightness']) for x in os.listdir(dir_path) if 'psu' in x]
    if 'psuX_led/brightness' in check_list:
        check_list.remove('psuX_led/brightness')
        for attr in attrX:
            check_list.append(arrt)
    for attr in check_list[2:]:
        attr = attr.strip()
        file_path = os.path.join(dir_path, attr)
        info = read_info(file_path)
        write_log(info[0], info[1])
    write_log('')
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
    check_list = config_split()
    check_config(check_list)


