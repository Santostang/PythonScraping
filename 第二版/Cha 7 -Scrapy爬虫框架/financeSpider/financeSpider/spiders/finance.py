# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from financeSpider.items import FinancespiderItem

class FinanceSpider(scrapy.Spider):
    name = 'finance'
    allowed_domains = ['finance.eastmoney.com']
    start_urls = ['http://finance.eastmoney.com/news/cywjh_1.html']
    url_head = 'http://finance.eastmoney.com/news/cywjh_'
    url_end = '.html'

    # Scrapy自带功能，从start_requests开始发送请求
    def start_requests(self):
        #获取前三页的url地址
        for i in range(1,4):
            url = self.url_head + str(i) + self.url_end
            print ("当前的页面是：", url)
            # 对新闻列表页发送Request请求
            yield scrapy.Request(url=url, callback = self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        title_list = soup.find_all("p", class_="title")
        for i in range(len(title_list)):
            # 将数据封装到FinancespiderItem对象，字典类型数据
            item = FinancespiderItem()
            title = title_list[i].a.text.strip()
            link = title_list[i].a["href"]
            # 变成字典
            item["title"] = title
            item["link"] = link   
            # 根据文章链接，发送Request请求，并传递item参数     
            yield scrapy.Request(url=link, meta = {'item':item}, callback = self.parse2)

    def parse2(self, response):
        #接收传递的item
        item = response.meta['item']
        #解析提取文章内容
        soup = BeautifulSoup(response.text, "lxml")
        content = soup.find("div", id="ContentBody").text.strip()
        content = content.replace("\n", " ")
        item["content"] = content
        #返回item，交给item pipeline
        yield item
