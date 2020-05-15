import logging
import time
import traceback
from functools import wraps
from gauto import manager

device = manager.get_device()
engine = manager.get_engine()
logger = logging.getLogger("wetest")

def launch_game_and_catch_exception(is_relunch):
    def old_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            while True:
                try:
                    st = time.time()
                    ret = device.is_app_launched()
                    if ret is False:
                        device.launch_app()
                    timeout = 20 * 60
                    ret = engine.wait_sdk_wake_up(timeout)
                    if not ret:
                        logger.error("GA 组件启动超时")
                        return
                    else:
                        logger.info(f"GA组件启动成功，耗时 {time.time() - st} s")

                    func()  # 执行脚本
                    break
                except Exception as e:
                    logger.error(f"catch Exception : {e}")
                    stack = traceback.format_exc()
                    logger.exception(stack)

                    if is_relunch:
                        logger.info("重启游戏")
                        logger.info("GAutomation Message:Output Log")
                        time.sleep(5)
                        device.relaunch_app()
            logger.info("GameEnd")
        return wrapper
    return old_wrapper