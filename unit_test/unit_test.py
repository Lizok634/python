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

ERRNO ={'EPATH':1, 'EEMPTY':2, 'EVALUE':3, 'EINVALID':4}  #err number

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
def write_log(attr, ret = -1, value = None, refer = '----'):
    try:
        log = open(log_file, 'a')
        if ret == 0:        #open file success,  write info to the log file
            log.write('{0:<22}{1:<32}{2:<18}{3:<6}{4}'.format(attr, \
                    value, refer, '[pass]', '\n'))
            print '{0:<22}{1:<32}{2:<18}{3:<6}'.format(attr, value, \
                    refer, '[pass]')
        if ret == 1:        #sysfs path or file is not exist
            log.write('{0:<22}{1:<50}{2}'.format(attr, ' is not exist', \
                    '[*fail*]\n'))
            print '{0:<22}{1:<50}{2}'.format(attr,' is not exist', '[*fail*]')
        if ret == 2:        #open file fail, an empty file
            log.write('{0:<22}{1:<32}{2:<18}{3:<6}'.format(attr, '----', \
                    refer, '[fail]\n'))
            print '{0:<22}{1:<32}{2:<18}{3:<6}'.format(attr, '----', \
                    refer, '[*fail*]')
        if ret == 3:        #error value
            log.write('{0:<22}{1:<32}{2:<18}{3:<6}'.format(attr, value, \
                    refer, '[*fail*]\n'))
            print '{0:<22}{1:<32}{2:<18}{3:<6}'.format(attr, value, \
                    refer, '[*fail*]')
        if ret == 4:        #error invalid value
            log.write('{0:<22}{1:<32}{2:<18}{3:<6}'.format(attr, value, \
                    refer, '[invalid]\n'))
            print '{0:<22}{1:<32}{2:<18}{3:<6}'.format(attr, value, \
                    refer, '[invalid]')
        if ret == -1:       #print info without prefix
            log.write(attr + '\n')
            print attr
    except IOError:
        print "open log file fail"
        os._exit(-1)
    return log

#check path
def check_path(check_list):
    unit_name = check_list[0].replace('#####','').strip()   #get unit name
    write_log('{0:^72}'.format(unit_name))
    dir_path = check_list[1].strip()    #joint path
    if os.path.exists(dir_path) == False:   #check path exist or not
        write_log(dir_path, 1)
        write_log('')
        return dir_path, ERRNO['EPATH'] 
    else:
        return dir_path, 0

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
        return value, ERRNO['EPATH']

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

#check value 
def check_value(attr, value, refer):
    if len(value) == 0:
        return ERRNO['EEMPTY']
    if 'max' in refer and 'char' in refer:
        refer = (re.findall(r'\d+',refer))
        refer[0] = int(refer[0])
        if len(value) <= refer:
            return 0
    elif '-' in refer:
        if '-' in value:    #judge for negative number
            value = int(value)
        elif value.isdigit():
            value = int(value)
        else:
            return ERRNO['EEMPTY']
        refer = re.findall(r'\d+',refer)
        refer[0] = int(refer[0])
        refer[1] = int(refer[1])
        if 'temp' in attr:
            if value > -1*refer[0] and value <= refer[1]:
                return 0
            elif value == -128000:
                return ERRNO['EINVALID']
            else:
                return ERRNO['EVALUE']
        elif 'fault' in attr:
            if value == 0:
                return 0
            elif value == 1:    #XXX_fault = 1  represent device XXX is fault
                return ERRNO['EVALUE']
        else:
            if value >= int(refer[0]) and value <= int(refer[1]):
                return 0
            else:
                return ERRNO['EVALUE']
    return

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
    ret = check_path(check_list)
    if ret[1] != 0:
        return
    dir_path = ret[0]
    write_log('{0:<22}{1:<32}{2:<18}{3:<8}'.format('items',\
                'value','reference', 'result'))
    for line in check_list[2:]:
        line = line.strip().split('\t')
        attr = line[0]
        file_path = os.path.join(dir_path, attr)
        info = read_info(file_path)
        value = info[0]
        ret = info[1]
        if len(line) == 2:
            refer = line[1].strip()
            ret = check_value(attr, value, refer)
            write_log(attr, ret, value, refer)
        else:
            write_log(attr, ret, value)
    write_log('')
    return

#check psu
def check_psu(check_list):
    ret = check_path(check_list)
    if ret[1] != 0:
        return
    dir_path = ret[0]

    psu_num = os.listdir(dir_path)
    for psu in psu_num:
        X = psu.replace('psu', '')  #get psu num
        psu_path = os.path.join(dir_path, psu)  #joint psu path
        tip = ''.join(['#****************', psu, '****************#'])
        write_log('{0:^72}'.format(tip))
        write_log('{0:<22}{1:<32}{2:<18}{3:<8}'.format('items', \
                'value','reference', 'result'))
        attrX = [''.join(x) for x in os.listdir(psu_path) \
                            if 'fan' in x or 'temp' in x]
        attrX.sort()
        tmp_list = copy.deepcopy(check_list)    #copy check_list to tmp_list
        tmp_list.extend(attrX)

        refer_tempX_input = ''
        refer_fanX_input = ''
        refer_fanX_pwm = ''
        refer_fanX_fault = ''

        for line in tmp_list[2:]:
            line = line.strip().split('\t')
            attr = line[0]
            refer = '----'
            if len(line) == 2:
                refer = line[1].strip()
            if 'tempX_input' in attr:     #record reference
                refer_tempX_input = refer
                continue
            elif 'fanX_input' in attr:
                refer_fanX_input = refer
                continue
            elif 'fanX_pwm' in attr:
                refer_fanX_pwm = refer
                continue
            elif 'fanX_fault' in attr:
                refer_fanX_fault = refer
                continue
            elif 'X' in attr:
                continue

            if 'temp' in attr and 'input' in attr:
                refer = refer_tempX_input
            elif 'fan' in attr and 'input' in attr:
                refer = refer_fanX_input
            elif 'fan' in attr and 'pwm' in attr:
                refer = refer_fanX_pwm
            elif 'fan' in attr and 'fault' in attr:
                refer = refer_fanX_fault
            file_path = os.path.join(psu_path, attr)
            info = read_info(file_path)
            value = info[0]
            ret = info[1]
            if 'present' in attr and info[0] == '0':
                log = ''.join([psu, ' is not present'])
                write_log(log)
                break
            else:
                ret = check_value(attr, value, refer)
                write_log(attr, ret, value, refer)
    write_log('')
    return

#check ports sfp or qsfp
def check_Xsfp(check_list, modu_type):
    ret = check_path(check_list)
    if ret[1] != 0:
        return
    dir_path = ret[0]

    portX = os.listdir(dir_path)
    for port in portX:
        file_path = os.path.join(dir_path, port, 'identifier')#check ports type
        info = read_info(file_path)
        modu_id = info[0]
        if modu_id != '3':
            modu_id = '4'
        if modu_id == modu_type:
            #tip = ''.join(['#********', port, '********#'])
            #write_log(tip)
            line = check_list[2].strip()
            line = line.strip().split('\t')
            attr = line[0]
            file_path = os.path.join(dir_path, port, attr)
            info = read_info(file_path)
            value = info[0]
            if value == '0':  #check module plug in or out
                #log = ''.join(['     module plug out     '])
                #write_log(log)
                #write_log('')
                pass
            else:
                tip = ''.join(['#****************', port, '****************#'])
                write_log('{0:^72}'.format(tip))
                write_log('{0:<22}{1:<32}{2:<18}{3:<8}'.format('items', \
                        'value','reference', 'result'))
                for line in check_list[2:]:
                    line = line.strip().split('\t')
                    attr = line[0]
                    refer = '----'
                    if len(line) == 2:
                        refer = line[1].strip()
                    file_path = os.path.join(dir_path, port, attr)
                    info = read_info(file_path)
                    value = info[0]
                    ret = check_value(attr, value, refer)
                    write_log(attr, ret, value, refer)
        else:
            continue
    write_log('')
    return

#check ctrl
def check_ctrl(check_list):
    ret = check_path(check_list)
    if ret[1] != 0:
        return
    dir_path = ret[0]

    fan_number = 0
    fanr_number = 0
    refer = '----'

    write_log('{0:<22}{1:<32}{2:<18}{3:<8}'.format('items', \
                'value','reference', 'result'))
    line = check_list[2].strip().split('\t')    #get fan number
    attr = line[0]
    if len(line) == 2:
        refer = line[1].strip()
    file_path = os.path.join(dir_path, attr)
    info = read_info(file_path)
    value = info[0]
    ret = info[1]
    if value.isdigit() and int(value) < 20:#fan number must be a digist
        fan_number = info[0]
        ret = check_value(attr, value, refer)
        write_log(attr, ret, value, refer)
    else:
        write_log('fan number error')
        return

    line = check_list[3].strip().split('\t')    #get fanr number
    attr = line[0]
    if len(line) == 2:
        refer = line[1].strip()
    file_path = os.path.join(dir_path, attr)
    info = read_info(file_path)
    value = info[0]
    ret = info[1]
    if info[0].isdigit() and int(info[0]) < 20:#fanr number must be a digist
        fanr_number = info[0]
        ret = check_value(attr, value, refer)
        write_log(attr, ret, value, refer)
    else:
        write_log('fanr number error')
        return

    for line in check_list[4:]:
        line = line.strip().split('\t')
        attr = line[0]
        refer = '----'
        if len(line) == 2:
            refer = line[1].strip()
        if 'fanX' in attr:  #get fanX info
            n = 1
            while n <= int(fan_number):
                attrX = attr.replace('X',str(n))
                file_path = os.path.join(dir_path, attrX)
                info = read_info(file_path)
                value = info[0]
                ret = check_value(attr, value, refer)
                write_log(attrX, ret, value, refer)
                n += 1
        elif 'fanrX' in attr:   #get fanrX info
            n = 1
            while n <= int(fanr_number):
                attrX = attr.replace('X',str(n))
                file_path = os.path.join(dir_path, attrX)
                info = read_info(file_path)
                value = info[0]
                ret = check_value(attr, value, refer)
                write_log(attrX, ret, value, refer)
                n += 1
        else:
            file_path = os.path.join(dir_path, attr)
            info = read_info(file_path)
            value = info[0]
            ret = check_value(attr, value, refer)
            write_log(attr, ret, value, refer)
    write_log('')
    return

#check leds
def check_leds(check_list):
    ret = check_path(check_list)
    if ret[1] != 0:
        return
    dir_path = ret[0]

    write_log('{0:<22}{1:<32}{2:<18}{3:<8}'.format('items', \
                'value','reference', 'result'))
    attrX = [''.join([x, '/brightness'])    \
                for x in os.listdir(dir_path) if 'psu' in x]
    
    check_list.extend(attrX)
    refer_psuX_led = ''
    
    for line in check_list[2:]:
        line = line.strip().split('\t')
        attr = line[0]
        refer = '----'
        if len(line) == 2:
            refer = line[1].strip()
        if 'psuX_led' in attr:
            refer_psuX_led = refer 
            continue
        elif 'X' in attr:
            continue

        if 'psu' in attr and 'led' in attr:
            refer = refer_psuX_led
        
        file_path = os.path.join(dir_path, attr)
        info = read_info(file_path)
        value = info[0]
        ret = check_value(attr, value, refer)
        write_log(attr, ret, value, refer)
    write_log('')
    return

#check watchdog
def check_watchdog(check_list):
    ret = check_path(check_list)
    if ret[1] != 0:
        return
    dir_path = ret[0]

    write_log('{0:<22}{1:<32}{2:<18}{3:<8}'.format('items', \
                'value','reference', 'result'))
    attr = check_list[2].strip()
    file_path = os.path.join(dir_path, attr)
    info = read_info(file_path)
    value = info[0]
    ret = info[1]

    if int(info[0]) == 1:
        write_log(attr, 0,'enable')
    elif int(info[0]) == 0:
        write_log(attr, 3,'disable')
    else:
        write_log(attr, ret, value)
    write_log('')
    return

#main function entry
if __name__=="__main__":
    init_log()
    check_list = config_split()
    check_sysfs(check_list)


