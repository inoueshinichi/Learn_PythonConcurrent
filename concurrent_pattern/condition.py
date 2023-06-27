"""条件変数によるスレッド制御
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


class Producer(threading.Thread):
    def __init__(self, 
                 stocks: deque, 
                 lock_cond: threading.Condition,
                 event: threading.Event,
                 ):
        super(Producer, self).__init__()
        self.stocks = stocks
        self.lock_cond = lock_cond
        self.event = event
        self.max_product: int = 5

    # override
    def run(self):
        count: int = 0
        self.event.set() # set True
        while True:
            if self.lock_cond.acquire():
                products = [randint(0, 100) for _ in range(5)]
                self.stocks.append(products)
                print('[{}th] 生産者{}は{}を生産した。'.format(count+1, self.name, self.stocks))
                self.lock_cond.notify()
                self.lock_cond.release()
                count += 1
                if count > self.max_product:
                    print('生産終了')
                    self.event.clear() # set False
                    break
            time.sleep(3) # 3sec

class Consumer(threading.Thread):
    def __init__(self, 
                 stocks: deque, 
                 lock_cond: threading.Condition,
                 event: threading.Event,
                 ):
        super(Consumer, self).__init__()
        self.stocks = stocks
        self.lock_cond = lock_cond
        self.event = event

    # override
    def run(self):
        self.event.wait() # 生産者が生産を開始するまで待機
        while self.event.isSet():
            self.lock_cond.acquire()
            if len(self.stocks) == 0:
                # 商品が無くなったら生産されるまで待つ
                # notfifyされるまでスレッドをハングアップ
                self.lock_cond.wait()
            print('お客様{}は{}を買った。在庫: {}'.format(self.name, self.stocks.popleft(), self.stocks))
            self.lock_cond.release()
            time.sleep(0.5) # 生産者(Producer)より消費者(Consumer)の方が消費サイクルが早い


class ConditionControlThreadsApp:

    # ストリームデータ
    stocks = deque()

    # 条件変数
    lock_cond = threading.Condition()

    # イベント
    event = threading.Event()

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

        producer = Producer(ConditionControlThreadsApp.stocks,
                            ConditionControlThreadsApp.lock_cond,
                            ConditionControlThreadsApp.event,
        )
        consumer = Consumer(ConditionControlThreadsApp.stocks,
                            ConditionControlThreadsApp.lock_cond,
                            ConditionControlThreadsApp.event,
        )

        producer.start()
        consumer.start()

        producer.join()
        consumer.join()

        print("[primary-thread] Shutdown producer-consumer system...")


if __name__ == "__main__":
    print(f"Don't execute {__file__} directly.")