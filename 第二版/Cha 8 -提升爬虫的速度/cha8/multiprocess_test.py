#!/usr/bin/python
 # -*- coding: utf-8 -*-

from multiprocessing import Pool, Manager
import time
import requests

def crawler(q, index):
    Process_id = 'Process-' + str(index)
    while not q.empty():
        url = q.get(timeout=2)
        try:
            r = requests.get(url, timeout=20)
            print (Process_id, q.qsize(), r.status_code, url)
        except Exception as e: 
            print (Process_id, q.qsize(), url, 'Error: ', e)


def multiprocess_main(link_list, p_num):
    start = time.time() 
    manager = Manager()
    workQueue = manager.Queue(1000)

    # 填充队列
    for url in link_list:
        workQueue.put(url)

    print ("Started processes")
    pool = Pool(processes=p_num)
    for i in range(p_num):
        pool.apply_async(crawler, args=(workQueue, i))

    
    pool.close()
    pool.join()

    end = time.time()
    time_spend = end-start
    print ('Pool + Queue多进程爬虫的总时间为：', time_spend)
    print ('Main process Ended!')
    return time_spend

if __name__ == '__main__':
    link_list = []
    with open('alexa.txt', 'r') as file:
        file_list = file.readlines()
        for eachone in file_list:
            link = eachone.split('\t')[1]
            link = link.replace('\n','')
            link_list.append(link)

    multiprocess_main(link_list, 3)