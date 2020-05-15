import os
import logging
import subprocess
import time
import re
from .utils import retry_if_fail
logger=logging.getLogger("gauto")


def excute_adb(cmd, serial=None):
    if serial:
        command = "adb -s {0} {1}".format(serial, cmd)
    else:
        command = "adb {0}".format(cmd)
    file = os.popen(command)
    return file


@retry_if_fail()
def forward(pc_port, mobile_port):
    cmd = "forward tcp:{0} tcp:{1}".format(pc_port, mobile_port)
    excute_adb_process(cmd)
    return excute_adb_process("forward --list")

def remove_forward(pc_port):
    cmd = "forward --remove tcp:{0} ".format(pc_port)
    excute_adb_process(cmd)

def excute_adb_process_daemon(cmd, shell=False, serial=None, sleep=3 , needStdout=True):
    if serial:
        command = "adb -s {0} {1}".format(serial, cmd)
    else:
        command = "adb {0}".format(cmd)
    if needStdout is True:
        p = subprocess.Popen(command, shell=shell, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    else:
        p = subprocess.Popen(command, shell=shell)
    time.sleep(sleep)
    return p

def excute_adb_process(cmd, serial=None):
    if serial:
        command = "adb -s {0} {1}".format(serial, cmd)
    else:
        command = "adb {0}".format(cmd)

    ret = ""
    for i in range(0,3):
        p = subprocess.Popen(command, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        lines = p.stdout.readlines()
        ret = ""
        for line in lines:
            ret += line.decode() + "\n"
        if "no devices/emulators found" in ret or "device offline" in ret:
            logger.error("rety in excute_adb_process")
            time.sleep(20)
        else:
            return ret
    return ret

def excute_adb_process_communication(cmd, serial=None):
    command = construct_command(cmd, serial)
    logger.info(command)
    ret = ""
    p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p.communicate()
    if len(err) > 2:
        print(f"err : {err.decode('utf8','ignore')}")
    return out

def kill_process_by_name(name):
    logger.debug("shell ps "+name)
    file = excute_adb("shell ps")
    output = file.readlines()
    outstr = "\n".join(output)
    pattern = "\w+\s+(\d+)\s+.+"+name
    match = re.search(pattern, outstr, re.M)
    if match:
        pid = match.group(1)
        logger.debug("found process pid= {0}".format(pid))
        file = excute_adb("shell kill {0}".format(pid))
        logger.debug("kill process: {0}".format(file.readlines()))
        time.sleep(2)
    else:
        file = excute_adb("shell ps -ef")
        output = file.readlines()
        outstr = "\n".join(output)
        pattern = "\w+\s+(\d+)\s+.+" + name
        match = re.search(pattern, outstr, re.M)
        if match:
            pid = match.group(1)
            logger.debug("found process pid= {0}".format(pid))
            file = excute_adb("shell kill -9 {0}".format(pid))
            logger.debug("kill process: {0}".format(file.readlines()))
            time.sleep(2)

def kill_uiautomator():
    kill_process_by_name("uiautomator")

def get_device_time():
    device_time = None
    try:
        timeout = 3
        start = time.time()
        import subprocess
        process = subprocess.Popen('adb shell date ', shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        while process.poll() is None:
            time.sleep(0.2)
            if (time.time() - start) > timeout:
                os.kill(process.pid, 9)
                return None
        device_time_str = process.stdout.read().strip()
        device_time_str = device_time_str.decode('utf-8')
        logger.info(device_time_str)
        # 转为时间数组
        device_time_transed = device_time_str.split()
        device_time_str = "" + device_time_transed[1] + " " + device_time_transed[2] + " " +  device_time_transed[3] + " " + device_time_transed[5]
        print(device_time_str)
        timeArray = time.strptime(device_time_str, '%b %d %H:%M:%S %Y')
        # 转为时间戳
        device_time = int(time.mktime(timeArray))

        logger.info("device time: " + str(device_time))
    except Exception as e:
        logger.exception(e)
    return device_time
