# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BaidutbItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 关键字
    # keywords=Field()

    # 用户id
    author_name_id=Field()
    # 作者
    author_name=Field()

    # 文章内容
    title=Field()

    # 文章id
    content_ID=Field()
    # 文章内容
    content=Field()
    # 文章评论
    # comment=Field()
    # 楼数
    floor=Field()
    # 回复个数
    comment_num=Field()
    # 日期
    date=Field()

    # 页面url
    url=Field()

    # 贴吧明
    tb_name=Field()


