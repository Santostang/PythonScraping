#!/usr/bin/python
 # -*- coding: utf-8 -*-

import threading
import requests
import time
import queue as Queue


class myThread (threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q
    def run(self):
        print ("Starting " + self.name)
        while True:
            try:
                crawler(self.name, self.q)
            except:
                break
        print ("Exiting " + self.name)
        
def crawler(threadName, q):
    url = q.get(timeout=2)
    try:
        r = requests.get(url, timeout=20)
        print (q.qsize(), threadName, r.status_code, url)
    except Exception as e: 
        print (q.qsize(), threadName, url, 'Error: ', e)

def thread_main(link_list, t_num):
    start = time.time()
    workQueue = Queue.Queue(1000)
    threads = []

    # 创建新线程
    for tName in range(t_num):
        thread = myThread('Thread' + str(tName), workQueue)
        thread.start()
        threads.append(thread)
        
    # 填充队列
    for url in link_list:
        workQueue.put(url)

    # 等待所有线程完成
    for t in threads:
        t.join()

    end = time.time()
    print ('Queue多线程爬虫的总时间为：', end-start)
    print ("Exiting Main Thread")
    return end-start

if __name__ == '__main__':
    link_list = []
    with open('alexa.txt', 'r') as file:
        file_list = file.readlines()
        for eachone in file_list:
            link = eachone.split('\t')[1]
            link = link.replace('\n','')
            link_list.append(link)

    thread_main(link_list, 5)