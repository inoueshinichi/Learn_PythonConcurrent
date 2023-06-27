"""データ競合を防止する排他制御パターン
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


# Mutex
class MutexForDataRaceApp:
    # 貯金額
    balance : int = 0

    # Mutex
    lock = threading.Lock()  # ロックをインスタンス化

    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def change_it(cls, n : int):

        # ロックを取得
        MutexForDataRaceApp.lock.acquire()

        # Critical Section [Start]-----
        # 出金と入金でプラマイ0になるはず
        MutexForDataRaceApp.balance =  MutexForDataRaceApp.balance + n
        MutexForDataRaceApp.balance = MutexForDataRaceApp.balance - n
        # Critical Section [End]-----

        # ロックを解放
        MutexForDataRaceApp.lock.release()

    @classmethod
    def run_thread(cls, n : int):
        for _ in range(100000):
            MutexForDataRaceApp.change_it(n)

    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        t1 = threading.Thread(target=MutexForDataRaceApp.run_thread, args=(5,))
        t2 = threading.Thread(target=MutexForDataRaceApp.run_thread, args=(8,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        print('[primary-thread] 貯金額(with lock) balance=', MutexForDataRaceApp.balance)


# RecursiveMutex
class RecursiveMutexForDataRaceApp:
    # 貯金額
    balance : int = 0

    # RecursiveMutex
    rlock = threading.RLock()  # 再帰ロックをインスタンス化

    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def add_it(cls, n: int) -> int:
        # 再帰ロック
        RecursiveMutexForDataRaceApp.rlock.acquire()
        RecursiveMutexForDataRaceApp.balance = RecursiveMutexForDataRaceApp.balance + n
        return RecursiveMutexForDataRaceApp.balance
    
    @classmethod
    def sub_it(cls, n: int) -> int:
        # 再帰ロック
        RecursiveMutexForDataRaceApp.rlock.acquire()
        RecursiveMutexForDataRaceApp.balance = RecursiveMutexForDataRaceApp.balance - n
        return RecursiveMutexForDataRaceApp.balance

    @classmethod
    def change_it(cls, n : int):
        # ロックを取得
        RecursiveMutexForDataRaceApp.rlock.acquire()

        # Critical Section [Start]-----
        # 出金と入金でプラマイ0になるはず
        RecursiveMutexForDataRaceApp.balance = RecursiveMutexForDataRaceApp.add_it(n)
        RecursiveMutexForDataRaceApp.balance = RecursiveMutexForDataRaceApp.sub_it(n)
        # Critical Section [End]-----

        # 再帰的にロックを解放 (複数の再帰ロックを一括解放)
        RecursiveMutexForDataRaceApp.rlock.release()

    @classmethod
    def run_thread(cls, n : int):
        for _ in range(1000):
            RecursiveMutexForDataRaceApp.change_it(n)


    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        t1 = threading.Thread(target=RecursiveMutexForDataRaceApp.run_thread, args=(5,))
        t2 = threading.Thread(target=RecursiveMutexForDataRaceApp.run_thread, args=(8,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        print('[primary-thread] 貯金額(with recursive lock) balance=', RecursiveMutexForDataRaceApp.balance)




if __name__ == "__main__":
    print(f"Don't execute {__file__} directly.")