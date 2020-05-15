import wpyscripts.manager as manager

def start():
    engine = manager.get_engine()
    logger = manager.get_logger()

    epath = "/Canvas/Button"
    e = engine.find_element(epath)  # 查找物体
    logger.info(e)

    engine.click(e) # 点击物体

