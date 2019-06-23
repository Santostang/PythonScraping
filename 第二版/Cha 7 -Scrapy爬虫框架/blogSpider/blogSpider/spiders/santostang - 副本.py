import scrapy
import os
from bs4 import BeautifulSoup
from blogSpider.items import BlogspiderItem
# 设置相应的代理用户名密码，主机和端口号
os.environ['HTTP_PROXY'] = 'http://web-proxy.oa.com:8080'
os.environ['HTTPS_PROXY'] = 'https://web-proxy.oa.com:8080'


class SantostangSpider(scrapy.Spider):
    name = 'santostang'
    allowed_domains = ['www.santostang.com']
    start_urls = ['http://www.santostang.com/']

    def parse(self, response):
        # 第一部分代码：将html保存到本地
        # print (response.text)
        # filename = "index.html"
        # with open(filename, 'w', encoding="utf-8") as f:
        #     f.write(response.text)

        # 第二部分代码：打印文章标题
        # soup = BeautifulSoup(response.text, "lxml")
        # first_title = soup.find("h1", class_= "post-title").a.text.strip()
        # print ("第一篇文章的标题是：", first_title)
        # for i in range(len(title_list)):
        #     title = title_list[i].a.text.strip()
        #     print('第 %s 篇文章的标题是：%s' %(i+1, title))

        #存放文章信息的列表
        items = []

        soup = BeautifulSoup(response.text, "lxml")
        title_list = soup.find_all("h1", class_="post-title")
        for i in range(len(title_list)):
            # 将数据封装到BlogspiderItem对象，字典类型数据
            item = BlogspiderItem()
            title = title_list[i].a.text.strip()
            link = title_list[i].a["href"]
            # 变成字典
            item["title"] = title
            item["link"] = link
            items.append(item)
        
        # 返回数据
        return items



