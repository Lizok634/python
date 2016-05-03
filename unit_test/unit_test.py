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

#creat log file
try:
    log = open("check_log", 'w')
except IOError:
    print "creat log file failed"
    if log:
        log.close()
    os._exit(-1)

#path_name = '/sys/class/swmon/hwinfo/'
path_name = '/sys/class/hwmon/hwmon0/'

#path check
if os.path.exists(path_name) == False:
    print "%s is not exist" %path_name
    log.write(path_name + '\n')
    log.close()
    os._exit(-1)

#get config file path
config_path = os.getcwd()
#print config_path

#read hwinfo to match system's hwinfo
with open('config', 'r') as f:
    for line in f.readlines()[1:9]:
        check_list = line.strip().split('=')
        tmp = os.path.join(path_name, check_list[0]) 
        try:
            f1 = open(tmp, 'r')
            if check_list[1] == f1.read().strip():
                log.write(check_list[0] + '\t' + "ok" + '\n')
            else:
                log.write(check_list[0] + '\t' + "failed" + '\t')
                log.write('\"' + f1.read().strip() + '\"' + '\t' + '\n')
        except IOError:
                print '%s is not exit' %check_list[0]
                log.write(check_list[0] + ' is not exit' + '\n')
        #finally:
            #if f1:
             #   f1.close()
       # print(tmp)



