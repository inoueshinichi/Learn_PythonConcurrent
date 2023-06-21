"""スレッドアプリケーション
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


# 最も簡単なスレッドアプリケーション
class SimpleThreadApp:
    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def run(cls, n : str):
        # threading.current_thread().nameは, getName()を呼び出す
        print("task: {} (thread name: {})".format(
            n, threading.current_thread().name
        ), flush=True)

        time.sleep(1)
        print('2s', flush=True)
        time.sleep(1)
        print('1s', flush=True)
        time.sleep(1)
        print('0s', flush=True)
        time.sleep(1)

    def main(self):
        """アプリケーション
        """

        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        # Thread
        t1 = threading.Thread(target=SimpleThreadApp.run, args=("t1",))
        t2 = threading.Thread(target=SimpleThreadApp.run, args=("t2",), name="Thread T2") # ここではsetName()が呼び出される

        # start()
        t1.start()
        t2.start()

        # join()
        t1.join()
        t2.join()

        # メインスレッドは待機...
        print('main-thread waiting...')

        print(threading.current_thread().name)


# スレッドのカスタマイズ(threding.Threadクラスの継承)
class MyThread(threading.Thread):
    def __init__(self, n : str):
        super(MyThread, self).__init__()
        self.n : str = n

    # override
    def run(self):
        print("task: {} (thread name: {})".format(
            self.n, threading.current_thread().name
        ), flush=True)

        time.sleep(1)
        print('2s', flush=True)
        time.sleep(1)
        print('1s', flush=True)
        time.sleep(1)
        print('0s', flush=True)
        time.sleep(1)

# クラススタイルのスレッドを実行するアプリ
class ClassStyleThreadApp:
    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        t1 = MyThread("t1")
        t2 = MyThread("t2")

        # start
        t1.start()
        t2.start()

        # join
        t1.join()
        t2.join()

        # メインスレッドは待機...
        print('[primary-thread] waiting...')

        print(threading.current_thread().name)


# 実行中のスレッド数をカウントするアプリ
class CountingThreadApp:
    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    
    @classmethod
    def run(cls, n : str):
        print("task: {}".format(n))
        time.sleep(1)

    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))


        for i in range(1,4):
            t = threading.Thread(target=CountingThreadApp.run, args=("t{}".format(i),))
            t.start()

        time.sleep(0.5)

        print(f"[primary-thread] active_threads [{threading.active_count()}]" )


# デーモンスレッドを実行するアプリ
# デーモンスレッドは, プライマリースレッドが終了するまで待機する
class DaemonThreadApp:
    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')
    
    @classmethod
    def run(cls, n : str):
        print("task: {}".format(n))
        time.sleep(1)
        print('3')
        time.sleep(1)
        print('2')
        time.sleep(1)
        print('1')

    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        for i in range(1,4):
            t = threading.Thread(target=DaemonThreadApp.run, args=("t{}".format(i),))
            t.setDaemon(True) # Daemon
            t.start()

        time.sleep(1.5)
        print("[primary-thread] スレッド数: {}".format(threading.active_count()))


if __name__ == "__main__":
    print(f"Don't execute {__file__} directly.")
