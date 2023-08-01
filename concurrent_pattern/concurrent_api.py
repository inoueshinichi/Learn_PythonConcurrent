"""cuncurrent標準モジュールの使い方
"""
from concurrent.futures import thread
import os
import sys

# os.sepはプラットフォーム固有の区切り文字(Windows: `\`, Unix: `/`)
module_parent_dir = os.sep.join([os.path.dirname(__file__), '..'])
print("module_parent_dir", module_parent_dir)
sys.path.append(module_parent_dir)
# print("paths: \n", sys.path)

# from ..log_conf import logging
# log = logging.getLogger(__name__)
# # log.setLevel(logging.WARN)
# # log.setLevel(logging.INFO)
# log.setLevel(logging.DEBUG)

# ターゲットのモジュール
from concurrent.futures import (
    ThreadPoolExecutor, 
    ProcessPoolExecutor,
    as_completed,
    wait,
    ALL_COMPLETED,
    FIRST_COMPLETED,
    FIRST_EXCEPTION,
)

# Web リクエスト
import requests

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

# from ..type_hint import *


class ConcurrentApiOneTaskApp:

    def __init__(self, sys_argv = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def load_url(cls, url):
        # ワーカーで実行する処理
        print('[Start] Worker thread', flush=True)

        # HTTPによるURLリクエスト
        return requests.get(url)


    def main(self):
        """アプリケーション
        """
        # log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))
        print('[Start] main process')


        url = 'https://www.python.org/'

        # ワーカープール(プロセス)を4つ作成
        executor = ProcessPoolExecutor(max_workers=4)  # ThreadPoolExecutor(max_workers=4)

        # プールされているワーカーのどれか一つにタスクを投げる. Futureインスタンスで結果を受け取る
        future = executor.submit(ConcurrentApiOneTaskApp.load_url, url)
        print(future)

        while 1:
            if future.done():
                print('status code: {}'.format(future.result().status_code))
                break

        print("[End] main process")


class ConcurrentApiMultiTaskApp:

    URLS = ['https://google.com/', 'https://www.python.org/', 'https://api.github.com/']

    def __init__(self, sys_argv = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def load_url(cls, url):
        # ワーカーで実行する処理
        print('[Start] Worker thread', flush=True)

        # HTTPによるURLリクエスト
        return requests.get(url)


    def main(self):
        """アプリケーション
        """
        # log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))
        print('[Start] main process')

        # mapで複数タスクをプールワーカーに投げる
        with ProcessPoolExecutor(max_workers=4) as executor:
            for url, data in zip(ConcurrentApiMultiTaskApp.URLS, 
                                executor.map(ConcurrentApiMultiTaskApp.load_url, 
                                            ConcurrentApiMultiTaskApp.URLS)):
                print('{} - status_code {}'.format(url, data.status_code))

        print("[End] main process")

class ConcurrentApiMultiTaskAsCompletedApp:

    URLS = ['https://google.com/', 'https://www.python.org/', 'https://api.github.com/']

    def __init__(self, sys_argv = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def load_url(cls, url):
        # ワーカーで実行する処理
        print('[Start] Worker thread', flush=True)

        # HTTPによるURLリクエスト
        return url, requests.get(url).status_code


    def main(self):
        """アプリケーション
        """
        # log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))
        print('[Start] main process')


        # プールされているワーカーのどれか一つにタスクを投げる. Futureインスタンスで結果を受け取る
        # mapで複数タスクをプールワーカーに投げる
        # with ProcessPoolExecutor(max_workers=4) as executor:
        #     for url, data in zip(ConcurrentApiMultiTaskApp.URLS, 
        #                         executor.map(ConcurrentApiMultiTaskApp.load_url, 
        #                                     ConcurrentApiMultiTaskApp.URLS)):
        #         print('{} - status_code {}'.format(url, data.status_code))

        with ProcessPoolExecutor(max_workers=4) as executor:
            tasks = [executor.submit(ConcurrentApiMultiTaskAsCompletedApp.load_url, url)
                    for url in ConcurrentApiMultiTaskAsCompletedApp.URLS]
            for future in as_completed(tasks):
                print(*future.result())

        print("[End] main process")


class ConcurrentApiMultiTaskWaitApp:

    URLS = ['https://google.com/', 'https://www.python.org/', 'https://api.github.com/']

    def __init__(self, sys_argv = None):
        if sys_argv is None:
            sys_argv = sys.argv[1:]

        parser = argparse.ArgumentParser()

        # 必要であれば, ここにアプリ引数を登録

        self.cli_args = parser.parse_args(sys_argv)
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    @classmethod
    def load_url(cls, url):
        # ワーカーで実行する処理
        print('[Start] Worker thread', flush=True)

        # HTTPによるURLリクエスト
        # return url, requests.get(url).status_code

        requests.get(url)
        print(url)


    def main(self):
        """アプリケーション
        """
        # log.info("Starting {}, {}".format(type(self).__name__, self.cli_args))
        print('[Start] main process')


        # プールされているワーカーのどれか一つにタスクを投げる. Futureインスタンスで結果を受け取る
        # mapで複数タスクをプールワーカーに投げる
        # with ProcessPoolExecutor(max_workers=4) as executor:
        #     for url, data in zip(ConcurrentApiMultiTaskApp.URLS, 
        #                         executor.map(ConcurrentApiMultiTaskApp.load_url, 
        #                                     ConcurrentApiMultiTaskApp.URLS)):
        #         print('{} - status_code {}'.format(url, data.status_code))

        # with ProcessPoolExecutor(max_workers=4) as executor:
        #     tasks = [executor.submit(ConcurrentApiMultiTaskAsCompletedApp.load_url, url)
        #             for url in ConcurrentApiMultiTaskAsCompletedApp.URLS]
        #     for future in as_completed(tasks):
        #         print(*future.result())

        with ProcessPoolExecutor(max_workers=4) as executor:
            tasks = [executor.submit(ConcurrentApiMultiTaskAsCompletedApp.load_url, url) 
                     for url in ConcurrentApiMultiTaskAsCompletedApp.URLS]
            wait(tasks, return_when=ALL_COMPLETED)
            print('all completed.')  # 3つのprintの後にメインプロセスが解放されprintする

        print("[End] main process")

# if __name__ == "__main__":
#     app = ConcurrentApiOneTaskApp()
#     app.main()

