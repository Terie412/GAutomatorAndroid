# GAutomatorAndroid
[![Wetest](https://img.shields.io/badge/wetest-2.8.2-green.svg)](wetest.qq.com)  [![license](https://img.shields.io/badge/license-mit-red.svg)](https://github.com/Tencent/tinker/blob/master/LICENSE)

GAutomator 的简化版本。保留了绝大部分的本地核心功能。删除了对python2的兼容。删除了对云平台的支持。

### 最简单的使用

脚本的入口是main.py，一个简单的启动例子如下（一般来说这个例子中展示的参数都是必需的）：
```shell script
python main.py --serial=emular-5554 --localport=53001 --sample=test_engine --package=com.tencent.sgame --mainactivity=com.tencent.sgame.MainActivity
```
脚本的参数说明如下：

|参数|参数缩写|说明|
|------|------|------|
|--qqname|-q|登录游戏的时候的QQ账户|
|--qqpwd|-p|登录游戏的时候的QQ密码|
|--wechataccount|-b|登录游戏的时候的微信账户|
|--wechatpwd|-c|登录游戏的时候的微信密码|
|--localport|-e|建立adb forward转发时的本地端口|
|--serial|-s|设备序列号|
|--sample|-m|要运行的测试用例|
|--package|-k|游戏的包名|
|--mainactivity|-j|游戏的主Activity，可以问客户端程序拿到|


测试用例的根脚本写在test_sample目录下，--sample后面跟测试用例的名称即可，他会启动测试用例中的`start()`方法。

### Device API

|Device API|说明|
|---|---|
|launch_app|拉起APP|
|is_app_launched|判断app是否启动|
|relaunch_app|重启app|
|kill_app|杀死app进程|
|get_screenshot|截屏（稍慢，adb自带）|
|mini_screencap|截屏（很快，minicap的功能，可能有兼容性问题）|

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

### 一个简单的测试用例的例子
```python
import logging,traceback, random, re, time, os
from gauto import manager

device = manager.get_device()
engine = manager.get_engine()
logger = logging.getLogger("wetest") # 全局默认的logger名称都是wetest

def start():
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
```
