#!/usr/bin/python
 # -*- coding: utf-8 -*-

import gevent
from gevent.queue import Queue, Empty
import time
import requests

from gevent import monkey#把下面有可能有IO操作的单独做上标记
monkey.patch_all() # 将IO转为异步执行的函数

start = time.time()
workQueue = Queue(1000)
def crawler(index):
    Process_id = 'Process-' + str(index)
    while not workQueue.empty():
        url = workQueue.get(timeout=2)
        try:
            r = requests.get(url, timeout=20)
            print (Process_id, workQueue.qsize(), r.status_code, url)
        except Exception as e: 
            print (Process_id, workQueue.qsize(), url, 'Error: ', e)

def boss(link_list):
    for url in link_list:
        workQueue.put_nowait(url)

def gevent_main(link_list, g_num):
    gevent.spawn(boss,link_list).join()
    jobs = []
    for i in range(g_num):
        jobs.append(gevent.spawn(crawler, i))
    gevent.joinall(jobs)

    end = time.time()
    time_spend = end-start
    print ('gevent + Queue多协程爬虫的总时间为：', time_spend)
    print ('Main Ended!')
    return time_spend

if __name__ == '__main__':
    link_list = []
    with open('alexa.txt', 'r') as file:
        file_list = file.readlines()
        for eachone in file_list:
            link = eachone.split('\t')[1]
            link = link.replace('\n','')
            link_list.append(link)

    

    gevent_time10 = gevent_main(link_list, 15)
    print ('gevent + Queue多协程爬虫的总时间为：', gevent_time10)

    gevent_time3 = gevent_main(link_list, 20)
    print ('gevent + Queue多协程爬虫的总时间为：', gevent_time3)

    with open('result_gevent.txt','a+',encoding='utf-8') as f:
        f.write('\t' + str(gevent_time10) + '\t' + str(gevent_time3))