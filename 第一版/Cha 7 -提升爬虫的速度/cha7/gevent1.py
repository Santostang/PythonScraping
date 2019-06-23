import gevent
from gevent.queue import Queue, Empty
import time
import requests

from gevent import monkey#把下面有可能有IO操作的单独做上标记
monkey.patch_all() # 将IO转为异步执行的函数

link_list = []
with open('alexa.txt', 'r') as file:
    file_list = file.readlines()
    for eachone in file_list:
        link = eachone.split('\t')[1]
        link = link.replace('\n','')
        link_list.append(link)

start = time.time()
def crawler(index):
    Process_id = 'Process-' + str(index)
    while not workQueue.empty():
        url = workQueue.get(timeout=2)
        try:
            r = requests.get(url, timeout=20)
            print (Process_id, workQueue.qsize(), r.status_code, url)
        except Exception as e: 
            print (Process_id, workQueue.qsize(), url, 'Error: ', e)

def boss():
    for url in link_list:
        workQueue.put_nowait(url)

if __name__ == '__main__':
    workQueue = Queue(1000)

    gevent.spawn(boss).join()
    jobs = []
    for i in range(10):
        jobs.append(gevent.spawn(crawler, i))
    gevent.joinall(jobs)

    end = time.time()
    print ('gevent + Queue多协程爬虫的总时间为：', end-start)
    print ('Main Ended!')
