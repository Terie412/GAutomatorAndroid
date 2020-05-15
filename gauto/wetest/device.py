from gauto.common.adb_process import *
import numpy as np
import cv2

class Device(object):
    def __init__(self, serial, package, main_activity):
        self.serial = serial
        self.package = package
        self.main_activity = main_activity
        self.last_launch_time = 0
        self.time_sleep = 15
        self.win_size = self.get_win_size()
        self.sdk_version = self.get_sdk_version()
        self.init_minicap()

    def kill_app(self):
        logger.info("杀死游戏进程...")
        ret = self.is_app_launched()
        if ret is False:
            return 0

        pid = self.get_pid()
        cmd = f"shell am force-stop {self.package}"
        print(f"cmd = {cmd}")
        excute_adb_process(cmd, self.serial)

    def relaunch_app(self):
        self.kill_app()
        time.sleep(2)
        self.launch_app()

    def get_pid(self):
        ret = excute_adb_process(f"shell ps | findstr {self.package}")
        if self.package in ret:
            pid = ret.split()[1]
            logger.info(f"get_pid : {pid}")
            return pid
        return ""

    def launch_app(self):
        logger.info("启动游戏...")
        excute_adb_process(f"shell am start -n {self.package}/{self.main_activity}", self.serial)

    # def is_app_launched(self):
        # ret = excute_adb_process(f"shell ps")
        # if self.package in ret:
        #     return True
        # return False

    def is_app_launched(self):
        """
        在很多游戏中，除了游戏本身的进程之外，还会开启别的进程，比如腾讯的信鸽，分包下载用的乐变。
        有些进程在游戏退出之后仍然在后台运作，这些进程的名字往往都是 [游戏包名:other_name] 的形式，
        所以原本判断包名是否在进程列表中的方法在很多场合就行不通了
        """
        ret = excute_adb_process(f"shell ps")
        ret += excute_adb_process(f"shell pf -ef")

        s1 = re.findall(self.package, ret)
        s2 = re.findall(self.package+":", ret)
        if len(s2) < len(s1):
            return True
        return False

    def get_screenshot(self, save_path: str):
        excute_adb_process("shell screencap -p /sdcard/screen.png")
        time.sleep(2)
        excute_adb_process(f"pull /sdcard/screen.png {save_path}")
        time.sleep(1)

    def get_sdk_version(self):
        sdk_version = excute_adb_process("shell getprop ro.build.version.sdk").rstrip("\r\n\n")
        if not str.isalnum(sdk_version):
            logger.error(f"获取sdk版本失败 : {sdk_version}")
            sdk_version = 23
        else:
            logger.info(f"sdk version = {sdk_version}")
            sdk_version = int(sdk_version)
        return sdk_version

    def get_win_size(self):
        ret = excute_adb_process("shell wm size", self.serial)
        nums = re.findall(r"\d+", ret)
        if len(nums) < 2:
            logger.error("初始化分辨率失败")
            return (1920, 1080)
        num1 = int(nums[0])
        num2 = int(nums[1])
        return  (num1, num2) if num1 > num2 else (num2, num1)

    def init_minicap(self):
        # 防止重复push，节省时间，注释掉的话，每次初始化都会push一遍
        # content = excute_adb_process("shell ls /data/local/tmp", self.serial)
        # if 'minicap.so' in content:
        #     self.if_minicap_init = True
        #     return

        abi = excute_adb_process("shell getprop ro.product.cpu.abi", self.serial)
        sdk_version = excute_adb_process("shell getprop ro.build.version.sdk", self.serial)
        abi = abi.lstrip("b'").rstrip("\\r\\r\\n'\n")
        sdk_version = sdk_version.lstrip("b'").rstrip("\\r\\r\\n'\n")

        minicap_path = f"./libs/stf_libs/{abi}/minicap"
        if not os.path.exists(minicap_path):
            logger.error(f"没有成功加载minicap: {minicap_path}")
        minicap_so_path = f"./libs/stf_libs/minicap-shared/aosp/libs/android-{sdk_version}/{abi}/minicap.so"
        if not os.path.exists(minicap_so_path):
            logger.error(f"没有成功加载minicap.so: {minicap_so_path}")
        excute_adb_process(f"push {minicap_path} /data/local/tmp/", self.serial)
        excute_adb_process(f"push {minicap_so_path} /data/local/tmp/", self.serial)
        excute_adb_process(f"shell chmod 777 /data/local/tmp/minicap", self.serial)
        excute_adb_process(f"shell chmod 777 /data/local/tmp/minicap.so", self.serial)
        self.if_minicap_init = True

    def mini_screencap(self, save_path, size=(256, 144)):
        """
        截图
        save_path 截图保存路径；size 图片保存的大小
        """
        num1 = self.win_size[0]
        num2 = self.win_size[1]
        cmd = f"shell LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P {num1}x{num2}@{num1}x{num2}/0 -s"
        raw_data = excute_adb_process_communication(cmd, self.serial)

        line_break = "\r\n"
        if self.sdk_version < 24:
            line_break = "\r" + line_break

        jpg_data = raw_data.split(b"for JPG encoder" + line_break.encode())[-1]
        jpg_data = jpg_data.replace(line_break.encode(), b"\n")

        nparr = np.frombuffer(jpg_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img = cv2.resize(img, size)
        cv2.imwrite(save_path, img)


