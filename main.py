import logging,os,importlib,os,traceback,getopt,sys, optparse

os.chdir(os.path.dirname(os.path.abspath(__file__)))
logger = logging.getLogger("wetest")

def _run():
    model_path = os.environ.get("GA_SAMPLE", "")
    if model_path == "":
        return
    model_path = 'test_sample.' + model_path

    print(f"执行测试样例 : {model_path}\n")
    m = importlib.import_module(model_path)
    m.start()
    pass


def main():
    usage = "usage:%prog [options] --qqname= --qqpwd= --engineport= --uiport= --serial="
    parser = optparse.OptionParser(usage)
    parser.add_option("-q", "--qqname", dest="GA_QQNAME", help="QQ Account")
    parser.add_option("-p", "--qqpwd", dest="GA_QQPWD", help="QQ Password")
    parser.add_option("-k", "--package", dest="PKGNAME", help="upload password")
    parser.add_option("-j", "--mainactivity", dest="LAUNCHACTIVITY", help="upload password")
    parser.add_option("-b", "--wechataccount", dest="GA_WECHATNAME", help="wechat Account")
    parser.add_option("-c", "--wechatpwd", dest="GA_WECHATPWD", help="wechat Password")
    parser.add_option("-e", "--localport", dest="GA_LOCAL_PORT", help="network port forward engine sdk")
    parser.add_option("-s", "--serial", dest="GA_SERIAL", help="adb devices android mobile serial")
    parser.add_option("-m", "--sample", dest="GA_SAMPLE", help="the test sample you are going to test")
    (options, args) = parser.parse_args()
    try:
        if options.GA_QQNAME:
            os.environ["GA_QQNAME"] = options.GA_QQNAME
        if options.GA_QQPWD:
            os.environ["GA_QQPWD"] = options.GA_QQPWD
        if options.GA_WECHATNAME:
            os.environ["GA_WECHATNAME"] = options.GA_WECHATNAME
        if options.GA_WECHATPWD:
            os.environ["GA_WECHATPWD"] = options.GA_WECHATPWD
        if options.GA_LOCAL_PORT:
            os.environ["GA_LOCAL_PORT"] = options.GA_LOCAL_PORT
        if options.GA_SERIAL:
            os.environ["GA_SERIAL"] = options.GA_SERIAL
        if options.GA_SAMPLE:
            os.environ["GA_SAMPLE"] = options.GA_SAMPLE
        if options.PKGNAME:
            os.environ["PKGNAME"] = options.PKGNAME
        if options.LAUNCHACTIVITY:
            os.environ["LAUNCHACTIVITY"] = options.LAUNCHACTIVITY
    except getopt.error as e:
        print("for help use --help")
        return 2

    try:
        _run()
    except:
        stack = traceback.format_exc()
        logger.exception(stack)
    finally:
        logger.debug("GAutomator End")


if __name__ == "__main__":
    sys.exit(main())
