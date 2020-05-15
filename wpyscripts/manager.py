__author__ = 'minhuaxu wukenaihesos@gmail.com'

import traceback

from wpyscripts.wetest.device import *
from wpyscripts.wetest.engine import *

device = None
engine = None

def forward():
    local_port = os.environ.get("GA_LOCAL_PORT", "53001")
    cmd = f"forward tcp:{local_port} tcp:{27019}"
    ret = ""
    while True:
        ret = excute_adb_process(cmd)
        logger.info(f"ret of adb forward = \n{ret}")
        if "already" in ret.lower():
            local_port = int(local_port) + 1
            cmd = f"forward tcp:{local_port} tcp:{27019}"
            ret = excute_adb_process(cmd)
        else:
            break
    os.environ["GA_LOCAL_PORT"] = str(local_port)
    cmd = f"forward --list"
    ret = excute_adb_process(cmd)
    logger.info(f"the list of adb forward:\n{ret}")


def remove_forward():
    local_port = os.environ.get("GA_LOCAL_PORT", "53001")
    cmd = f"forward --remove tcp:{local_port}"
    excute_adb_process(cmd)

def get_device():
    global device
    if device is not None:
        return device
    pkgname = os.environ.get("PKGNAME", "")
    launch_activity = os.environ.get("LAUNCHACTIVITY", "")
    serial = os.environ.get("GA_SERIAL")

    device = Device(serial, pkgname, launch_activity)
    return device

def get_engine():
    """
    无论游戏启不启动，engine都应该能够正常初始化的，因为socket只是跟forward是否成功转发端口有关
    :return: UnityEngine(GameEngine)
    """
    global engine
    if engine:
        return engine

    for i in range(2):
        try:
            forward()
            local_port = int(os.environ.get("GA_LOCAL_PORT", "53001"))
            engine = UnityEngine(address="127.0.0.1", port=int(local_port))
            break
        except Exception as e:
            stack = traceback.format_exc()
            logger.exception(stack)
            logger.error(e)
    return engine
