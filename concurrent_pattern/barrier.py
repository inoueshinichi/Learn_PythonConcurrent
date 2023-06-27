"""バリア制御
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
from random import randint
from collections import deque

import numpy as np
import scipy as np

from type_hint import *


class Player(threading.Thread):
    def __init__(self, id: int, 
                 barrier: threading.Barrier,
                 ):
        super(Player, self).__init__(name='Player {}'.format(id))
        self.barrier = barrier

    def run(self):
        try:
            if not self.barrier.broken:
                print('{}さんが参加しました。'.format(self.name))
                self.barrier.wait(3) # 3秒でタイムアウト(バリアから抜ける)
                print('{}さんゲーム開始'.format(self.name))

        except threading.BrokenBarrierError:
            print('ゲーム開始できないため、{}が退出しました。'.format(self.name))



def barrier_action():
    print('参加者が集まりました. ゲームを開始します.')

class BarrierGamePlayersJoinApp:

    lock = threading.Lock()

    # バリア
    barrier = threading.Barrier(parties=4, action=barrier_action)

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

        players = []
        for i in range(10):
            p = Player(i, BarrierGamePlayersJoinApp.barrier)
            players.append(p)

        for p in players:
            p.start()

if __name__ == "__main__":
    print(f"Don't execute {__file__} directly.")