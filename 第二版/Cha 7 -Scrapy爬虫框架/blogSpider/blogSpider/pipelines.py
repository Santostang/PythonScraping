# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BlogspiderPipeline(object):
    #填入你的地址
    file_path = "C:/Users/santostang/Desktop/blogSpider/result.txt"

    def __init__(self):
        self.article = open(self.file_path, "a+", encoding="utf-8")

    #定义管道的处理方法
    def process_item(self, item, spider):
        title = item["title"]
        link = item["link"]
        content = item["content"]
        output = title + '\t' + link + '\t' + content + '\n\n'
        self.article.write(output)
        return item
