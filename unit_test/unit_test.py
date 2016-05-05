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

log_name = 'check_log'

#init log file
def init_log():
    try:
        log = open(log_name, 'w')
        log.truncate()      #empty log file
    except IOError:
        print "open log file failed"
        os._exit(-1)
    return

#write log file
def write_log(info, num = -1):
    try:
        log = open(log_name, 'a')
        if num == 0:
            log.write("[failed]" + info + " is not exist"  + "\n")
            print ("[failed] " + info + " is not exist")
        if num == 1:
            log.write("[pass]" + info + "\n")
            print ("[pass] " + info)
        if num == 2:
            log.write("[failed]" + info + "\n")
            print ("[failed] " + info)
        if num == -1:
            log.write(info + "\n")
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
        tmp = ''.join([file_name, ' open failed'])
        return tmp, 2


#path_name = '/sys/class/swmon/hwinfo'
#path_name_test = '/sys/class/hwmon/hwmon0'

#split config file
def check_config():
    with open('config', 'r') as f:
        flag = 1
        unit_name = ''
        path_name = ''
        config_tab = f.readlines()
        for line in config_tab:
            line = line.strip()
            if flag == 1 and line.split(' ')[0] == '#####':
                unit_name = line
                print unit_name
                flag = 0
                continue
            elif flag == 1:
                continue

            if flag == 0:
                dir_path = line
                write_log(unit_name)
                if os.path.exists(dir_path):
                    flag = 2
                    continue
                else:
                    write_log(dir_path, 0)
                    flag = 1
                    continue

            if flag == 2:
                if line == '' or line == '\n':
                    flag = 1
                    print '\n'
                    write_log('')
                    continue
                else:
                    file_path = os.path.join(dir_path, line)
                    info = read_info(file_path)
                    write_log(info[0], info[1])
    return

'''
                split_count[j] = i + 1
                j = j + 1
        split_count[j] = i
   return split_count

        else:
            flag = 0
            check_list = line.strip().split('=')
        tmp = os.path.join(path_name, check_list[0])
        try:
            f1 = open(tmp, 'r')
            if check_list[1] == f1.read().strip():
                print "%-20s     pass" %check_list[0]
                log.write("[pass]" + check_list[0] + "\n")
            else:
                log.write(check_list[0] + '\t' + "failed" + '\t')
        except IOError:
                print "%-20s     failed" %check_list[0]
                log.write("[failed]" + check_list[0] + "\n")
        #finally:
            #if f1:
             #   f1.close()
       # print(tmp)
    retrun
'''

#check hwinfo information
#def check_hwinfo():



if __name__=="__main__":
    init_log()
    check_config()


