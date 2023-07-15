"""プロセス間通信
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
    Queue,
    Pipe,
    Value, # shared_memory
    Array, # shared_memory
    shared_memory, # Python >= 3.8
    Manager,
)

from multiprocessing.managers import (
    SharedMemoryManager, # Python >= 3.8
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


class ProcessConnectWithQueueApp: 
    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def write(cls, q : Queue):
        # Queueにデータを書き込む
        print('Process to write: {}'.format(os.getpid()))
        for value in ['A', 'B', 'C']:
            print('Put {} to queue...'.format(value))
            q.put(value)
            time.sleep(random.random())

    @classmethod
    def read(cls, q : Queue):
        # Queueからデータを読み取り
        print('Process to read: {}'.format(os.getpid()))
        while True: # イベント駆動
            value = q.get(True)
            print('Get {} from queue.'.format(value))

    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))


        # 親プロセスがQueueを作って、子プロセスに渡す
        q = Queue()
        pw = Process(target=ProcessConnectWithQueueApp.write, args=(q,))
        pr = Process(target=ProcessConnectWithQueueApp.read, args=(q,))

        # pwを起動し、書き込み開始
        pw.start()
        # prを起動し、読み取り開始
        pr.start()
        # pwが終了するのを待つ
        pw.join()
        # prは無限ループなので、強制終了
        pr.terminate()


class ProcessConnectWithPipeApp:
    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def subprocess_exec(cls, child_pipe_connect):
        child_pipe_connect.send([42, None, 'hello'])
        child_pipe_connect.close()

    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        parent_conn, child_conn = Pipe()
        p = Process(target=ProcessConnectWithPipeApp.subprocess_exec, args=(child_conn,))
        p.start()
        print(parent_conn.recv())
        p.join()


class ProcessConnectSharedMemoryApp:
    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def other_process_exec(cls, num : Value, array : Array):
        print('Process to other_process_exec: {}'.format(os.getpid()))
        num.value = 3.1415927
        for i in range(len(array)):
            array[i] = -array[i]

    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        num = Value('d', 0.0)  # double型数字
        arr = Array('i', range(10))  # 配列

        p = Process(target=ProcessConnectSharedMemoryApp.other_process_exec, args=(num, arr))
        p.start()
        p.join()

        print(num.value)
        print(arr[:])

    
class ProcessConnectWithNamedSharedMemoryApp:

    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def other_process_exec(cls):
        print('[Start] other_process {}'.format(os.getpid()))

        count : int = 0
        existing_shm = shared_memory.SharedMemory(name='shm') # shmという共有メモリを取得

        while True:
            c = np.ndarray((3, 3), dtype=np.float64, buffer=existing_shm.buf)

            print("other_process_exec: c\n", c)

            time.sleep(random.random())

            if count > 10:
                break

            count = count + 1

        print('[End] other process {}'.format(os.getpid()))


    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        a = np.ones((3,3), dtype=np.float64) # double ローカル

        # 名前付き共有メモリ
        shm = shared_memory.SharedMemory(create=True, size=a.nbytes, name='shm')

        p = Process(target=ProcessConnectWithNamedSharedMemoryApp.other_process_exec)
        p.start()
        

        b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)
        b[:] = a[:] # ローカルメモリを共有メモリにコピー

        time.sleep(0.5)

        print('main process b[:, 0] = 2')

        b[:, 0] = 2

        time.sleep(0.5)

        print('main process b[:, 1] = 2')

        b[:, 1] = 2

        time.sleep(0.5)

        print('main process b[:, 2] = 2')

        b[:, 2] = 2

        p.join()

        print('[End] main process')

# Topic形式
class ProcessConnectWithManagerApp:

    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def other_process_exec(cls, d: dict, l: list, i: int):
        print('[Start] other_process {}'.format(os.getpid()))

        d[i] = i
        d[str(i)] = str(i)
        l.append(i)
        print(l)


    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

        with Manager() as manager:
            shared_dict = manager.dict()
            shared_list = manager.list()
            p_list = []
            # 10個のプロセスを作成
            for i in range(10):
                p = Process(target=ProcessConnectWithManagerApp.other_process_exec, 
                            args=(shared_dict, shared_list, i))
                p.start()
                p_list.append(p)
            for p in p_list:
                p.join()

            print('All subprocesses done.')
            print(shared_dict)
            print(shared_list)


class ProcessConnectWithSharedMemoryManagerApp:

    def __init__(self, sys_argv : Optional[Any] = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser : Any = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def other_process_exec(cls, d: dict, l: list, i: int):
        print('[Start] other_process {}'.format(os.getpid()))

    def main(self):
        """アプリケーション
        """
        log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))

if __name__ == "__main__":
    print(f"Don't execute {__file__} directly.")