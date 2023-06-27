"""スレッドローカル変数
"""
from asyncio import Condition
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
from random import randint
from collections import deque

import numpy as np
import scipy as np

from type_hint import *


class ThreadLocalApp:
    # スレッドローカル
    local = threading.local()

    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def print_local_x(cls):
        x = ThreadLocalApp.local.x
        print('{}のx: {}\n'.format(threading.current_thread().name, x))


    @classmethod
    def set_thread_local_x(cls, x: int):
        ThreadLocalApp.local.x = x
        print('{}のxを設定しました'.format(threading.current_thread().name), flush=True)
        time.sleep(1)
        ThreadLocalApp.print_local_x()

    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        t1 = threading.Thread(target=ThreadLocalApp.set_thread_local_x, args=(5, ), name="Thread-A")
        t2 = threading.Thread(target=ThreadLocalApp.set_thread_local_x, args=(10, ), name="Thread-B")
        t1.start()
        t2.start()
        t1.join()
        t2.join()

if __name__ == "__main__":
    print(f"Don't execute {__file__} directly.")
