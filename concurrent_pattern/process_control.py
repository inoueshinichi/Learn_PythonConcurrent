"""プロセス制御
"""
from concurrent.futures import thread
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

from multiprocessing import (
    Process,
    Lock,
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


class ProcessLockApp:

    lock = Lock()

    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def other_process_exec(cls, i):
        print('[Start] other_process {}'.format(os.getpid()))

        # 共有資源は, 標準出力
        ProcessLockApp.lock.acquire()
        try:
            print('hello world', i)
        finally:
            ProcessLockApp.lock.release()

    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        for num in range(10):
            Process(target=ProcessLockApp.other_process_exec, args=(num,)).start()


# import task_server_master
# import task_client_worker
from concurrent_pattern import task_server_master
from concurrent_pattern import task_client_worker

# サーバープロセスとクライアントプロセス
class ProcessServerClientApp:

    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def client_process_exec(cls):
        print('[Start] client_process {}'.format(os.getpid()))

        # クラントプロセス起動
        task_client_worker.main()

    @classmethod
    def server_process_exec(cls):
        print('[Start] server_process {}'.format(os.getpid()))

        # サーバープロセス起動
        task_server_master.main()


    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        master_process = Process(target=ProcessServerClientApp.server_process_exec)
        worker_process = Process(target=ProcessServerClientApp.client_process_exec)
        master_process.start()
        time.sleep(1)
        worker_process.start()
        
        worker_process.join()
        master_process.join()

        print('Finish')

if __name__ == "__main__":
    print(f"Don't execute {__file__} directly.")