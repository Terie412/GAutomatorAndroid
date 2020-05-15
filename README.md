# GAutomatorAndroid
![PyPI - Downloads](https://img.shields.io/badge/qintianchen-gauto--android-orange)
[![0.1.2](https://img.shields.io/badge/version-v3.9.5-blue)](https://pypi.org/manage/project/gauto-android/releases/) 

[中文文档](./README_cn.md)

A simplified version of the Android script in GAutomator, removing support for the cloud platform, removing compatibility with python2.7, and modifying some interfaces.

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
logger = logging.getLogger("gauto") # The global default logger name is "gauto"

def init():
    os.environ["FORWARD_LOCAL_PORT"] = "53001" # Local port, one for each android device
    os.environ["ANDROID_SERIAL"] = "emulator-5554" # Android device serial number
    os.environ["PKGNAME"] = "com.tencent.sgame" # Package name
    os.environ["LAUNCHACTIVITY"] = "com.tencent.sgame.MainActivity" # Main Activity

def run():
    logger.info("Launch app")
    device.launch_app()
    time.sleep(2)

    logger.info("Click the button named Button.close")
    e = engine.find_element("/Canvas/Button.close")
    engine.click(e)

    logger.info("screenshot")
    device.mini_screencap("./screenshot.png")

    logger.info("Kill app")
    device.kill_app()

run()
```

### Another way to start your script —— Read the arguments from the command line

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

In the entry script above, your can code your automation logic in 'run()'. Before that, the script takes arguments from the command line and initializes some environment variables.The reason is simple, for some global environment variables are used in gauto-android package, and if you don't set the required global variables, you might get some exceptions.You can then launch it with the following command:

```shell script
python main.py --serial=emular-5554 --localport=53001 --package=com.tencent.sgame --mainactivity=com.tencent.sgame.MainActivity
```
The parameters of the script are described as follows:

|param|param abbreviation|description|
|------|------|------|
|--localport|-e|Establish a local port for adb forwarding|
|--serial|-s|Device serial number|
|--package|-k|Package name|
|--mainactivity|-j|Main activity, get it from client programmer|

### Device API

|Device API|description|
|---|---|
|launch_app|Launch APP|
|is_app_launched|Determine if the app is started|
|relaunch_app|Relaunch app|
|kill_app|Kill app process|
|get_screenshot|Screenshot (slightly slower, adb‘s built-in capabilities)|
|mini_screencap|Screenshot (good performance, but with possible compatibility issues)|

### Engine API
The Unity engine-related APIs are placed in the engine.py module

| Engine API | Description |
| ------| ------ |
| find_element | Gets an instance of an object by its fullpath |
| find_elements_path|Returns a list of objects that correspond to a particular fullpath (expression)|
|find_elements_by_component|Find the object by given type and return a list|
|get_element_bound|Gets the boundary information of the object|
|get_element_text|Returns the text of the TextView component on an object|
|get_element_image|Returns the texture name in the Render component on an object|
|get_scene|Gets the name of the current scene|
|get_element_world_bound|Gets the boundary information of the object in world coordinates|
|click_position|Click by coordinates|
|click|Click on the center of an object|
|press_position|Press by coordinate|
|press|Press the center of an object|
|swipe_position|Swipe by coordinates|
|swipe|Slide from the center of one object to the center of another|
|swipe_and_press|joystick simulation|
|input|Set the text for a TextView in an object|
|get_touchable_elements_bound|Gets the boundary information for all touchable objects|
|get_registered_handlers|Returns the list of name of the methods registered in SDK|
|call_registered_handler|Call a method registered in SDK|
|get_component_methods|Gets a list of method in a component|
|call_component_method|Gets a component's method to call a method on a component|

