"""サーバープロセス
managersでキューをAPIとしてインターネットに公開します。
サーバープロセスはキューを起動して、タスクを入れると、
他のマシンからアクセスすることが可能になります。
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

import random
import queue
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
    pass

# タスクを送るキュー
task_queue = queue.Queue()
def task_queue_func():
    return task_queue

# 結果を受け取るキュー
result_queue = queue.Queue()
def result_queue_func():
    return result_queue

def main():
    print('[START] Queue Server')

    # 2つのキューをAPIとして登録する
    # Windowsの場合はAPI登録にlambdaが使えないので、素直に関数を定義してください
    QueueManager.register('get_task_queue', callable=task_queue_func)
    QueueManager.register('get_result_queue', callable=result_queue_func)

    # ポート5000を使い、認証暗号を'abc'にする
    # Windowsの場合はアドレスを明記する必要がある（127.0.0.1)
    host: str = '127.0.0.1'
    port: int = 10000
    authkey: bytes = b'abc'
    manager = QueueManager(address=(host, port), authkey=authkey)

    # 起動する
    manager.start()

    # ネット経由でキューオブジェクトを取得
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    # タスクを入れてみる
    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task {}...'.format(n))
        task.put(n)

    # resultキューから結果を受け取る
    print('Try get results...')
    for i in range(10):
        # 10秒超えたらtimeoutで終了
        r = result.get(timeout=10)
        print('Result: {}'.format(r))

    # 終了
    manager.shutdown()
    print('master exit.')

    print('[END] Queue Server')
    
if __name__ == "__main__":
    main()