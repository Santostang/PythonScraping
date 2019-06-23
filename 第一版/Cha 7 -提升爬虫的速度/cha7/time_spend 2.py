from multiprocess_test import multiprocess_main
from thread_test import thread_main

if __name__ == '__main__':
    link_list = []
    with open('alexa.txt', 'r') as file:
        file_list = file.readlines()
        for eachone in file_list:
            link = eachone.split('\t')[1]
            link = link.replace('\n','')
            link_list.append(link)

    #single = single()
    #print ('串行的总时间为：', single)

    #thread_time = thread_main(link_list, 5)
    #print ('Queue多线程爬虫的总时间为：', thread_time)

    multiprocess_time = multiprocess_main(link_list, 3)
    #print ('Pool + Queue多进程爬虫的总时间为：', multiprocess_time)

    #gevent_time = gevent_main(link_list, 10)
    #print ('gevent + Queue多协程爬虫的总时间为：', gevent_time)

    #with open('result.txt','a+',encoding='utf-8') as f:
    #    f.write(single + '\t' + thread_time + '\t' + multiprocess_time + '\t' + gevent_time)