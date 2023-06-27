"""イベント
"""
import os
import sys

# os.sepはプラットフォーム固有の区切り文字(Windows: `\`, Unix: `/`)
module_parent_dir = os.sep.join([os.path.dirname(__file__), '..'])
print("module_parent_dir", module_parent_dir)
sys.path.append(module_parent_dir)

from log_conf import logging
log = logging.getLogger(__name__)
# log.setLevel(logging.WARN)
# log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

import threading

import datetime
import time
import argparse
import glob
import shutil
import re
import math
import hashlib
import socket

import numpy as np
import scipy as np

from type_hint import *


class EventApp:
    # イベント
    event = threading.Event()
    # スレッドフラグ
    running: bool = False

    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def lighter(cls):
        """青信号 True
           赤信号 False
        """

        loop_count: int = 0
        count: int = 0
        EventApp.event.set() # 初期値は青信号
        
        while EventApp.running:
            if 5 < count <= 10:
                # 赤信号にする
                EventApp.event.clear()  # 赤信号にする
                print("\33[41;1m赤信号...\033[0m")
            elif count > 10:
                # 青信号にする
                EventApp.event.set()  # 青信号にする
                count = 0
                
                # スレッド終了条件
                loop_count += 1
                print("loop_count: {}\n".format(loop_count))
                if loop_count > 1:
                    EventApp.running = False
            else:
                print("\33[42;1m青信号...\033[0m")

            time.sleep(1)
            count += 1

        print('Shutdown lighter-thread...')

    @classmethod
    def car(cls, name: str):
        while EventApp.running:
            if EventApp.event.is_set():  # 青信号がどうかをチェック
                print("[{}] 前進する...".format(name))
                time.sleep(1)
            else:
                print("[{}] 赤信号のため、信号を待つ...".format(name))
                EventApp.event.wait()
                # flag=Trueになるまでここでブロッキングする
                print("[{}] 青信号のため、前進開始...".format(name))

        print('Shutdown car-thread...')


    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        EventApp.running = True

        light = threading.Thread(target=EventApp.lighter,)
        light.start()

        car = threading.Thread(target=EventApp.car, args=("MINI",))
        car.start()

        light.join()
        car.join()

        print('[primary-thread] Shutdown...')