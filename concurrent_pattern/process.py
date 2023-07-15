"""子プロセスを生成する
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
from multiprocessing import (
    Process,
    Pool,
)

import os
import datetime
import time
import argparse
import glob
import shutil
import re
import math
import hashlib
import socket
import time
import random

import numpy as np
import scipy as np

from type_hint import *


class SubProcessApp:

    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def subprocess_exec(cls, name: str):
        """子プロセスが実行する処理

        Args:
            name (str): _description_
        """
        print('Run child process {} ({})...'.format(name, os.getpid()))

    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))


        print('Parent process {}.'.format(os.getpid()))
        p = Process(target=SubProcessApp.subprocess_exec, args=('sub-process',))
        print('Child process will start.')
        p.start()
        p.join()
        print('Child process end.')


class ProcessPoolApp:

    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def subprocess_exec(cls, name: str):
        """子プロセスが実行する処理

        Args:
            name (str): _description_
        """
        print('Run task {} ({})...'.format(name, os.getpid()))
        start = time.time()
        time.sleep(random.random() * 3)
        end = time.time()
        print('Task {} runs {} seconds.'.format(name, (end - start)))

    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        print('Parent process {}.'.format(os.getpid()))
        p = Pool(4)  # 同時に最大4個の子プロセス
        for i in range(5):
            p.apply_async(ProcessPoolApp.subprocess_exec, args=(i,))
        # 非同期処理のため、親プロセスは子プロセスの処理を待たずに、
        # 次のprintをする

        print('Waiting for all subprocesses done...')
        p.close()
        p.join()
        print('All subprocesses done.')


if __name__ == "__main__":
    print(f"Don't execute {__file__} directly.")