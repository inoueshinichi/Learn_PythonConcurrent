"""ワーカープロセス
サーバープロセスが提供するWeb APIを通じたキューを使用する
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


import time
import queue
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
    pass

def main():
    print('[START] Worker Process')
    # 同じQueueManagerを作る
    

    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')

    # サーバーアクセス
    host: str = '127.0.0.1'
    port: int = 10000
    authkey: bytes = b'abc'

    print('Connect to server ({},{})...'.format(host, port))

    # 同じポートと認証暗号を設定する
    m = QueueManager(address=(host, port), authkey=authkey)

    # 接続
    m.connect()

    # それぞれのキューを取得
    task = m.get_task_queue()
    result = m.get_result_queue()

    # taskキューからタスクを受け取って
    # 処理結果をresultキューに格納する
    for i in range(10):
        try:
            n = task.get(timeout=1)
            # ここでは簡単な二乗計算をタスクとする
            print('run task {} * {}...'.format(n, n))
            r = '{} * {} = {}'.format(n, n, n*n)
            time.sleep(1)
            result.put(r)
        except queue.Empty:
            print('task queue is empty.')

    # 終了
    print('worker exit.')
    print('[END] Worker Process')

if __name__ == "__main__":
    main()