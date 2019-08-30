# -*- coding: utf-8 -*-
import configparser
import os
import win32service
import win32serviceutil
import win32event
from logger import logger

# config
configPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "settings.conf")
config = configparser.RawConfigParser()
config.read(configPath, "utf-8")

# log
logPath = config.get("logging", "logPath")
rotateWen = config.get("logging", "rotateWen")
rotateCount = int(config.get("logging", "rotateCount"))
log = logger("windowsServiceExample", logPath, rotateWen, rotateCount)

# サービス稼動中かどうかのイベント
hWaitStop = None

class testClass:
    # コンストラクタ
    def __init__(self):
        self.interval = int(config.get("general", "interval"))

    # ループを定期的に回す関数
    def run(self):
        cnt = 0

        while True:
            try:
                # ここに処理を書く
                log.info("loop cnt:" + str(cnt))
                cnt += 1
            except:
                log.traceback()

            # 指定チェック間隔時間で待機
            log.info("%d秒待機します..." % self.interval)
            eventRet = win32event.WaitForSingleObject(hWaitStop, self.interval * 1000)
            if eventRet == win32event.WAIT_OBJECT_0:
                # サービス終了
                return

# サービス化のためのクラス
class windowsServiceExample(win32serviceutil.ServiceFramework):
    _svc_name_ = config.get("service", "name")
    _svc_display_name_ = config.get("service", "dispName")
    _svc_description_ = config.get("service", "description")

    # コンストラクタ
    def __init__(self, args):
        global config
        global hWaitStop
        global log
        win32serviceutil.ServiceFramework.__init__(self, args)
        # サービス起動時はイベントを非シグナルで作成
        hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    # サービス開始時に呼ばれる。この関数を抜けるとプロセスが終了する
    def SvcDoRun(self):
        log.info("Service start.")
        tc = testClass()
        tc.run()
        log.info("Service exit.")

    # サービス終了時に呼ばれる関数
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # イベントをシグナル状態にすることでrun()内のループを抜ける
        win32event.SetEvent(hWaitStop)

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(windowsServiceExample)
