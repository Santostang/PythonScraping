import requests
from bs4 import BeautifulSoup
import re
import time
from redis import Redis
headers={ 'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36' }

def push_redis_list():
    r = Redis(host='137.189.204.65', port=6379 ,password='redisredis')
    print (r.keys('*'))
    
    link_list = []
    with open('alexa.txt', 'r') as file:
        file_list = file.readlines()
        for eachone in file_list:
            link = eachone.split('\t')[1]
            link = link.replace('\n','')
            link_list.append(link)
            if len(link_list) == 100:
                break
                
    for url in link_list:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'lxml')
        img_list = soup.find_all('img')
        for img in img_list:
            img_url = img['src']
            if img_url != '':
                print ("加入的图片url: ", img_url)
                r.lpush('img_url',img_url)
        print ('现在图片链接的个数为', r.llen('img_url'))
    return

def get_img():
    r = Redis(host='137.189.204.65', port=6379 ,password='redisredis')
    while True:
        try:
            url = r.lpop('img_url')
            url = url.decode('ascii')
            if url[:2] == '//':
                url = 'http:' + url
            print (url)
            try:
                response = requests.get(url, headers=headers,timeout = 20)
                name = int(time.time())
                f = open(str(name)+ url[-4:], 'wb')
                f.write(response.content)
                f.close()
                print ('已经获取图片', url)
            except Exception as e:
                print ('爬取图片过程出问题', e)
            time.sleep(3)
        except Exception as e:
            print (e)
            time.sleep(10)
            break
    return 

if __name__ == '__main__':           
    this_machine = 'slave'          
    print ('开始分布式爬虫')
    if this_machine == 'master':
        push_redis_list()
    else:
        get_img()