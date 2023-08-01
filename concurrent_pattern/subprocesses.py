"""subprocess標準モジュールの使い方
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

# ターゲットのモジュール
import subprocess

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


class SubProcessExternalCommandApp:

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

        # カレントディレクトリの確認
        print("[Start] subprocess 0")
        cmdlist = ['pwd']
        cp0 = subprocess.run(cmdlist, stdout=subprocess.PIPE)
        print('stdout:\n{}'.format(cp0.stdout.decode()))
        
        # subprocess.PIPEで標準出力をキャッチする.（キャッチしないと出力が捨てられる）
        print("[Start] subprocess 1")
        cmdlist = ['ls', '-la']
        cp1 = subprocess.run(cmdlist, stdout=subprocess.PIPE)
        print('stdout:\n{}'.format(cp1.stdout.decode()))

        # CompletedProcessの__repr__
        print("[Start] subprocess 2")
        cmdlist = ["ls", "-l", "/dev/null"]
        cp2 = subprocess.run(cmdlist, stdout=subprocess.PIPE)
        print("[Subprocess 2]:", cp2)

        # checkをTrueにすると、ステータスコードが0以外の時にエラーを起こす.
        print("[Start] subprocess 3")
        cp2 = subprocess.run("exit 1", shell=True, check=True)


class SubProcessPopenExternalCommandApp:

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

        # 標準入力、標準出力、標準エラーにパイプを繋ぐ
        print("[Start] python process")
        p = subprocess.Popen(["python"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 標準入力にデータを書き込む
        p.stdin.write(b'print("stdin")\n')
        # communicateの入力としてデータを渡す
        out, err = p.communicate(input=b'print("communicate")\n')
        print(out.decode())

        # | を使ったパイプライン処理は2つの子プロセスの標準出力と標準入力をパイプで繋ぐことで構築可能です
        print('[Start] df -h | grep Data')
        # 2つの子プロセスをパイプで繋ぐ
        p1 = subprocess.Popen(['df', '-h'], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(['grep', 'Data'], stdin=p1.stdout, stdout=subprocess.PIPE)
        out, err = p2.communicate()  # df -h | grep Data
        print(out.decode())
        
