"""スレッドによるマルチタスクによるデータ競合
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

# データ競合をわざと起こすアプリ
class DataRaceThreadApp:

    # 貯金額
    balance : int = 0

    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def change_it(cls, n : int):
        # 出金と入金でプラマイ0になるはず
        DataRaceThreadApp.balance =  DataRaceThreadApp.balance + n
        DataRaceThreadApp.balance = DataRaceThreadApp.balance - n

    @classmethod
    def run_thread(cls, n : int):
        for _ in range(100000):
            DataRaceThreadApp.change_it(n)

    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        t1 = threading.Thread(target=DataRaceThreadApp.run_thread, args=(5,))
        t2 = threading.Thread(target=DataRaceThreadApp.run_thread, args=(8,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        print('[primary-thread] 貯金額 balance=', DataRaceThreadApp.balance)

if __name__ == "__main__":
    print(f"Don't execute {__file__} directly.")