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

log_file = 'check_log'
config_file = 'config'

#init log file
def init_log():
    try:
        log = open(log_file, 'w')
        log.truncate()      #empty log file
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
        tmp = f.readline().splitlines()
        tmp = ''.join(tmp)
        tmp = ''.join([file_name,'=',tmp])
        return tmp, 1
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
    for tmp in check_list:
        if 'hwinfo' in tmp[0]:
            check_hwinfo(tmp)
        if 'psu' in tmp[0]:
            pass
            #check_psu(tmp)
        if 'ports' in tmp[0]:
            pass
            #check_ports()
    return

#check hwinfo 
def check_hwinfo(check_list):
    unit_name = check_list[0].strip()
    write_log(unit_name)
    dir_path = check_list[1].strip()
    if os.path.exists(dir_path) == False:
        write_log(dir_path, 0)
        return
    for tmp in check_list[2:]:
        tmp = tmp.strip()
        file_path = os.path.join(dir_path, tmp)
        info = read_info(file_path)
        write_log(info[0], info[1])
    write_log('')
    return


if __name__=="__main__":
    init_log()
    check_list = config_split()
    check_config(check_list)


