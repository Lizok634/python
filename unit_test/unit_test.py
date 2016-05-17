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
import re
import copy
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

       #ip = os.popen('ifconfig | grep 10.10.51.')  #get box ip address
        #addr = ip.read();ip.close();addr = addr.split(' ')
        #ip = ''.join([x for x in addr if 'addr' in x])
        tmp = os.popen('ifconfig')  #get box ip address
        ip = tmp.read();tmp.close()
        ip = re.findall(r'addr:10.10.51.\w{1,3}', ip)
        ip = ''.join(ip)

        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time = ''.join(['time:', time])   #get current time
        info = ''.join(['# ', box, '  ', version, '\n# ', ip, '  ', time])
        write_log(info)
        write_log('')
    except IOError:
        print "open log file fail"
        os._exit(-1)
    return

#write log file
def write_log(attr, value = None, ret = -1):
    if value == '':
        ret = 2
    try:
        log = open(log_file, 'a')
        if ret == 0:        #open file success,  write info to the log file
            log.write('{0:<10}{1:<22}{2:<25}{3}'.format('[pass]',\
                        attr, value, '\n'))
            print '{0:<10}{1:<22}{2:<25}'.format('[pass]', attr, value)
        if ret == 1:        #sysfs path is not exist
            log.write('{0:<12}{1}{2}'.format('[fail]',\
                        attr, ' is not exist\n'))
            print '{0:<10}{1}{2}'.format('[fail]', attr,' is not exist')
        if ret == 2:        #open file fail, an empty file
            log.write('{0:<10}{1:<22}{2}'.format('[fail]', attr, 'NULL\n'))
            print '{0:<10}{1:<22}{2}'.format('[fail]', attr, 'NULL')
        if ret == 3:        #error value
            log.write('{0:<10}{1:<22}{2:<25}{3}'.format('[fail]',\
                        attr, value, '\n'))
            print '{0:<10}{1:<22}{2:<25}'.format('[fail]', info, value)
        if ret == -1:       #print info without prefix
            log.write(attr + '\n')
            print attr
    except IOError:
        print "open log file fail"
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
    value = '0'
    try:
        f = open(file_path, 'r')
        value = f.readline().splitlines()
        value = ''.join(value)
        f.close()
        return value, 0
    except IOError:
        #tmp = ''.join([file_name, ' open fail'])
        return value, 1

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

#check sysfs
def check_sysfs(check_list):
    for sys_path in check_list:
        if 'hwinfo' in sys_path[0]:     #hwinfo
            check_hwinfo(sys_path)
        elif 'psu' in sys_path[0]:      #psu
            check_psu(sys_path)
        elif 'sfp/sfp+' in sys_path[0]: #sfp
            check_Xsfp(sys_path, '3')
        elif 'qsfp' in sys_path[0]:     #qsfp
            check_Xsfp(sys_path, '4')
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
        write_log(dir_path, None, 1)
        write_log('')
        return
    write_log('{0:<10}{1:<22}{2:<15}'.format('status', 'items', 'value'))
    for attr in check_list[2:]:
        attr = attr.strip()
        file_path = os.path.join(dir_path, attr)
        info = read_info(file_path)
        write_log(attr, info[0], info[1])
    write_log('')
    return

#check psu
def check_psu(check_list):
    unit_name = check_list[0].strip()   #print unit test name
    write_log(unit_name)
    dir_path = check_list[1].strip()    #get unit test path
    if os.path.exists(dir_path) == False:   #check path exist or not
        write_log(dir_path, None, 1)
        write_log('')
        return
    psu_num = os.listdir(dir_path)
    for psu in psu_num:
        X = psu.replace('psu', '')  #get psu num
        psu_path = os.path.join(dir_path, psu)  #joint psu path
        tip = ''.join(['#********', psu, '********#'])
        write_log(tip)
        write_log('{0:<10}{1:<22}{2:<15}'.format('status', 'items', 'value'))
        attrX = [''.join(x) for x in os.listdir(psu_path) \
                            if 'fan' in x or 'temp' in x]
        attrX.sort()
        tmp_list = copy.deepcopy(check_list)#copy check_list to tmp_list
        tmp_list.extend(attrX)

        for attr in tmp_list[2:]:
            attr = attr.strip()
            if 'X' in attr:         #ignore contain X attr
                continue
            file_path = os.path.join(psu_path, attr)
            info = read_info(file_path)
            if 'present' in attr and info[0] == '0':
                log = ''.join([psu, ' is not present'])
                write_log(log)
                break
            else:
                write_log(attr, info[0], info[1])
    write_log('')
    return

#check ports sfp or qsfp
def check_Xsfp(check_list, modu_type):
    unit_name = check_list[0].strip()   #print unit test name
    write_log(unit_name)
    dir_path = check_list[1].strip()    #get unit test path
    if os.path.exists(dir_path) == False:   #check path exist or not
        write_log(dir_path, None, 1)
        write_log('')
        return
    portX = os.listdir(dir_path)
    for port in portX:
        file_path = os.path.join(dir_path, port, 'identifier')    #check ports type
        info = read_info(file_path)
        modu_id = info[0]
        if modu_id != '3':
            modu_id = '4'
        if modu_id == modu_type:
            #tip = ''.join(['#********', port, '********#'])
            #write_log(tip)
            attr = check_list[2].strip()    #check module plug in or out
            file_path = os.path.join(dir_path, port, attr)
            info = read_info(file_path)
            if info[0] == '0':
                #log = ''.join(['     module plug out     '])
                #write_log(log)
                #write_log('')
                pass
            else:
                tip = ''.join(['#********', port, '********#'])
                write_log(tip)
                write_log('{0:<10}{1:<22}{2:<15}'.format('status',\
                            'items', 'value'))
                for attr in check_list[2:]:
                    attr = attr.strip()
                    file_path = os.path.join(dir_path, port, attr)
                    info = read_info(file_path)
                    write_log(attr, info[0], info[1])
        else:
            continue
    write_log('')
    return

#check ctrl
def check_ctrl(check_list):
    unit_name = check_list[0].strip()   #print unit test name
    write_log(unit_name)
    dir_path = check_list[1].strip()    #get unit test path
    if os.path.exists(dir_path) == False:   #check path exist or not
        write_log(dir_path, None, 1)
        write_log('')
        return

    fan_number = 0
    fanr_number = 0

    write_log('{0:<10}{1:<22}{2:<15}'.format('status', 'items', 'value'))
    attr = check_list[2].strip()    #get fan number
    file_path = os.path.join(dir_path, attr)
    info = read_info(file_path)
    if info[0].isdigit() and int(info[0]) < 20:#fan number must be a digist
        fan_number = info[0]
        write_log(attr, info[0], info[1])
    else:
        write_log('fan number error')
        return

    attr = check_list[3].strip()    #get fanr number
    file_path = os.path.join(dir_path, attr)
    info = read_info(file_path)
    if info[0].isdigit() and int(info[0]) < 20:#fanr number must be a digist
        fanr_number = info[0]
        write_log(attr, info[0], info[1])
    else:
        write_log('fanr number error')
        return

    for attr in check_list[4:]:
        attr = attr.strip()
        if 'fanX' in attr:  #get fanX info
            n = 1
            while n <= int(fan_number):
                attrX = attr.replace('X',str(n))
                file_path = os.path.join(dir_path, attrX)
                info = read_info(file_path)
                write_log(attrX, info[0], info[1])
                n += 1
        elif 'fanrX' in attr:   #get fanrX info
            n = 1
            while n <= int(fanr_number):
                attrX = attr.replace('X',str(n))
                file_path = os.path.join(dir_path, attrX)
                info = read_info(file_path)
                write_log(attrX, info[0], info[1])
                n += 1
        else:
            file_path = os.path.join(dir_path, attr)
            info = read_info(file_path)
            write_log(attr, info[0], info[1])
    write_log('')
    return

#check leds
def check_leds(check_list):
    unit_name = check_list[0].strip()   #print unit test name
    write_log(unit_name)
    dir_path = check_list[1].strip()    #get unit test path
    if os.path.exists(dir_path) == False:   #check path exist or not
        write_log(dir_path, None, 1)
        write_log('')
        return
    write_log('{0:<10}{1:<22}{2:<15}'.format('status', 'items', 'value'))
    attrX = [''.join([x, '/brightness'])    \
                for x in os.listdir(dir_path) if 'psu' in x]
    if 'psuX_led/brightness\n' in check_list:
        check_list.remove('psuX_led/brightness\n')
        check_list.extend(attrX)
    for attr in check_list[2:]:
        attr = attr.strip()
        file_path = os.path.join(dir_path, attr)
        info = read_info(file_path)
        write_log(attr, info[0], info[1])
    write_log('')
    return

#check watchdog
def check_watchdog(check_list):
    unit_name = check_list[0].strip()   #print unit test name
    write_log(unit_name)
    dir_path = check_list[1].strip()    #get unit test path
    if os.path.exists(dir_path) == False:   #check path exist or not
        write_log(dir_path, None, 1)
        write_log('')
        return
    write_log('{0:<10}{1:<22}{2:<15}'.format('status', 'items', 'value'))
    attr = check_list[2].strip()
    file_path = os.path.join(dir_path, attr)
    info = read_info(file_path)

    if int(info[2]) == 1:
        write_log(attr, 'enable', 0)
    elif int(info[2]) == 0:
        write_log(attr, 'disable', 0)
    else:
        write_log(attr, info[0], info[1])
    write_log('')
    return

#main function entry
if __name__=="__main__":
    init_log()
    check_list = config_split()
    check_sysfs(check_list)


