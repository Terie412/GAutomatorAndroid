# GAutomatorAndroid
[![](https://img.shields.io/badge/qintianchen-gauto--android-orange)](https://pypi.org/manage/project/gauto-android/releases/)
[![](https://img.shields.io/badge/version-v0.1.4-blue)](https://pypi.org/manage/project/gauto-android/releases/) 

GAutomator中Android部分的脚本的简化版本，删除了对云平台的支持，删除了对python2.7的兼容，修改了部分接口。

### Download and Install

```shell script
pip install gauto-android
```

### the simplest usage

```python
import os
import gauto.manager as manager

device = manager.get_device()
engine = manager.get_engine()
logger = logging.getLogger("gauto") # 全局默认的logger名称都是gauto

def init():
    os.environ["FORWARD_LOCAL_PORT"] = "53001" # 本地端口，一台安卓设备分配一个
    os.environ["ANDROID_SERIAL"] = "emulator-5554" # 安卓设备序列号
    os.environ["PKGNAME"] = "com.tencent.sgame" # 游戏包名
    os.environ["LAUNCHACTIVITY"] = "com.tencent.sgame.MainActivity" # 游戏主Activity

def run():
    logger.info("启动 app")
    device.launch_app()
    time.sleep(2)

    logger.info("点击关闭按钮")
    e = engine.find_element("/Canvas/Button.close")
    engine.click(e)

    logger.info("截图")
    device.mini_screencap("./screenshot.png")

    logger.info("杀死 app")
    device.kill_app()

run()
```

### 另一种启动方式——从命令行读取参数

```python
import getopt
import optparse
import os
import gauto.manager as manager

os.chdir(os.path.dirname(os.path.abspath(__file__)))
logger = manager.logger

def run():
    # dosomething...
    pass

def main():
    usage = "usage:%prog [options] --qqname= --qqpwd= --engineport= --uiport= --serial="
    parser = optparse.OptionParser(usage)
    parser.add_option("-w", "--localport", dest="FORWARD_LOCAL_PORT", help="forward local port")
    parser.add_option("-s", "--serial", dest="ANDROID_SERIAL", help="adb devices android mobile serial")
    parser.add_option("-k", "--package", dest="PKGNAME", help="upload password")
    parser.add_option("-j", "--mainactivity", dest="LAUNCHACTIVITY", help="upload password")
    (options, args) = parser.parse_args()
    try:
        if options.FORWARD_LOCAL_PORT:
            os.environ["FORWARD_LOCAL_PORT"] = options.FORWARD_LOCAL_PORT
        if options.ANDROID_SERIAL:
            os.environ["ANDROID_SERIAL"] = options.ANDROID_SERIAL
        if options.PKGNAME:
            os.environ["PKGNAME"] = options.PKGNAME
        if options.LAUNCHACTIVITY:
            os.environ["LAUNCHACTIVITY"] = options.LAUNCHACTIVITY

    except getopt.error as msg:
        logger.info("for help use --help")
        return 2

    run()

if __name__ == "__main__":
    sys.exit(main())

```

在上面的入口脚本中，你的逻辑可以写在`run()`里面，在此之前，脚本从命令行中接收参数并初始化了一些环境变量。原因很简单，因为modules中使用到了一些全局的环境变量，如果你不设置所必需的全局变量，就会可能会出错。之后你可以用以下命令启动：
```shell script
python main.py --serial=emular-5554 --localport=53001 --package=com.tencent.sgame --mainactivity=com.tencent.sgame.MainActivity
```
脚本的参数说明如下：

|参数|参数缩写|说明|
|------|------|------|
|--localport|-e|建立adb forward转发时的本地端口|
|--serial|-s|设备序列号|
|--package|-k|游戏的包名|
|--mainactivity|-j|游戏的主Activity，可以问客户端程序拿到|

### Device API

|Device API|说明|
|---|---|
|launch_app|拉起APP|
|is_app_launched|判断app是否启动|
|relaunch_app|重启app|
|kill_app|杀死app进程|
|get_screenshot|截屏（稍慢，adb自带）|
|mini_screencap|截屏（性能很好，但是可能有兼容性问题）|

### Engine API
The Unity engine-related APIs are placed in the engine.py module

| Engine API | Description |
| ------| ------ |
| find_element | 通过物体的名称获取物体的实例 |
| find_elements_path|返回包含符合特殊路径（表达式）的所有物体的列表|
|find_elements_by_component|通过类型名称查找物体，返回列表|
|get_element_bound|获取物体的边界信息|
|get_element_text|返回一个物体上的TextView组件的文本|
|get_element_image|返回一个物体上的Render组件中的纹理名称|
|get_scene|获取当前场景的名称|
|get_element_world_bound|获取物体在世界坐标下的边界信息|
|click_position|按照坐标点击|
|click|点击一个物体的中心位置|
|press_position|按照坐标长安|
|press|长按一个物体的中心位置|
|swipe_position|按照坐标滑动|
|swipe|从一个物体的中心位置滑动到另一个物体的中心位置|
|swipe_and_press|模拟摇杆|
|input|为一个物体中的TextView设置文本|
|get_touchable_elements_bound|获取所有可点击的物体的边界信息|
|get_registered_handlers|返回sdk中注册了的方法的名称|
|call_registered_handler|调用一个sdk中注册的方法|
|get_component_methods|获取一个组件的方法|
|call_component_method|调用一个组件上的方法|

