#!/usr/bin/python
 # -*- coding: utf-8 -*-

import requests
import time
#from multiprocess_test import multiprocess_main
#from thread_test import thread_main

def single():
    start = time.time()
    for eachone in link_list:
        try:
            r = requests.get(eachone)
            print (r.status_code, eachone)
        except Exception as e: 
            print('Error: ', e)
    end = time.time()
    time_spend = end-start
    print ('串行的总时间为：', time_spend)
    return time_spend

if __name__ == '__main__':
    link_list = []
    with open('alexa.txt', 'r') as file:
        file_list = file.readlines()
        for eachone in file_list:
            link = eachone.split('\t')[1]
            link = link.replace('\n','')
            link_list.append(link)

    #thread_time10 = thread_main(link_list, 10)
    #print ('Queue多线程爬虫的总时间为：', thread_time10)

    #multiprocess_time10 = multiprocess_main(link_list, 10)
    #print ('Pool + Queue多进程爬虫的总时间为：', multiprocess_time10)

    #thread_time3 = thread_main(link_list, 3)
    #print ('Queue多线程爬虫的总时间为：', thread_time3)

    #multiprocess_time3 = multiprocess_main(link_list, 3)
    #print ('Pool + Queue多进程爬虫的总时间为：', multiprocess_time3)

    single_time = single()
    print ('串行的总时间为：', single_time)

    with open('result_single_time.txt','a+',encoding='utf-8') as f:
        f.write(str(single_time))
        #f.write(str(thread_time10) + '\t' + str(multiprocess_time10) + '\t' + str(thread_time3) + '\t' + str(multiprocess_time3))