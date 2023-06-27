"""有限セマフォ
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


class BoundedSemaphoreApp:

    # 有限セマフォ
    bound_semaphore = threading.BoundedSemaphore(5) # スレッドの同時アクセス数を5個に制限

    # 初期状態のスレッド数
    init_threads:int = 0

    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def run(cls, n: int):

        # セマフォのロック
        BoundedSemaphoreApp.bound_semaphore.acquire()

        # Critical Section [Start]-----
        time.sleep(1)
        threads = threading.active_count() - BoundedSemaphoreApp.init_threads
        print("current thread: {}, thread_count: {}\n".format(n, threads), flush=True)
        # Critical Section [End]-----

        # セマフォのリリース　
        BoundedSemaphoreApp.bound_semaphore.release()

    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        # 初期状態で立ち上がっているスレッド数
        BoundedSemaphoreApp.init_threads = threading.active_count()

        # 10個のスレッドを立ち上げる
        for i in range(10):
            t = threading.Thread(target=BoundedSemaphoreApp.run, args=("t-{}".format(i),))
            t.start()
        
        while threading.active_count() > BoundedSemaphoreApp.init_threads:
            # print(f"[primary-thread] thread_count: {threading.active_count()}", flush=True)
            pass
        else:
            print('[primary-thread] active_threads: {}'.format(threading.active_count() - BoundedSemaphoreApp.init_threads))
            print('-----全てのスレッドが終了した-----')

if __name__ == "__main__":
    print(f"Don't execute {__file__} directly.")
