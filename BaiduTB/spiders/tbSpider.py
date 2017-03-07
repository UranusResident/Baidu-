# -*- coding: utf-8 -*-


from scrapy.http import Request
from BaiduTB.items import BaidutbItem


import time
from scrapy.item import Item, Field
from selenium import webdriver

from scrapy.spiders import CrawlSpider,Rule

from scrapy.selector import HtmlXPathSelector

# from time import sleep
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import json
import random





class TbSpider(CrawlSpider):

	name="baidu"

	allowed_domains=["baidu.com"]

	start_urls=["http://tieba.baidu.com/f/search/res?isnew=1&kw=&qw=%D6%EC%B9%B2%C9%BD&rn=10&un=&only_thread=0&sm=1&sd=&ed=&pn=1"]




	User_Agent_List = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',\
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',\
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 "]

	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap["phantomjs.page.settings.userAgent"] = (random.choice(User_Agent_List))




	def parse(self,response):


		driver=webdriver.PhantomJS(desired_capabilities=self.dcap)

		driver.get(response.url)

		# 智能等待3秒
		# driver.implicitly_wait(3)

		item=BaidutbItem()

		try:

			lis=driver.find_elements_by_xpath("//div[@class='s_post']")

			for li in lis:

				span=li.find_element_by_xpath(".//span[@class='p_title']")

				a=span.find_element_by_xpath(".//a").get_attribute('href')

				item['title']=span.find_element_by_xpath('.//a').text

				item['date']=li.find_element_by_xpath('.//font[contains(@class,"p_green p_date")]').text

				item['tb_name']=li.find_element_by_xpath('.//a[@class="p_forum"]/font').text


				yield Request(a,callback = self.parse_post_content,meta={'item': item})

			next=driver.find_element_by_xpath('//a[@class="next"]').get_attribute('href')

			if next:
				print 'next===========>',next

				yield self.make_requests_from_url(next)

		except Exception, e:
			raise e
		finally:
			driver.quit()



	def parse_post_content(self,response):

		print 'doing........',response.url

		# item=BaidutbItem()
		item = response.meta['item']

		driver=webdriver.PhantomJS(desired_capabilities=self.dcap)

		driver.get(response.url)

		driver.implicitly_wait(4)

		has_comment=False



		try:
			section_div=driver.find_elements_by_xpath('//div[contains(@id,"j_p_postlist")]')


			item['url']=response.url



			for section in section_div:

				l_post=section.find_element_by_xpath('div').get_attribute('data-field')

				Data = json.loads(l_post)


				item['author_name_id']=Data['author']['user_id']

				item['author_name']=Data['author']['user_name']

				item['content_ID']=Data['content']['post_id']



				item['content'] = section.find_element_by_xpath(".//div[contains(@class,'j_d_post_content')]").text

				print 'content===========>',section.find_element_by_xpath(".//div[contains(@class,'j_d_post_content')]").text




				item['floor'] = Data['content']['post_no']

				item['comment_num'] = Data['content']['comment_num']

				if item['comment_num'] > 0:
					has_comment = True
				


				yield item

			# 如果有回复，继续爬取回复（查看更多需要登录)
			# if has_comment:
			# 	url = "http://tieba.baidu.com/p/totalComment?tid=%d&fid=1&pn=%d" % (meta['thread_id'], meta['page'])

			# 	yield scrapy.Request(url, callback = self.parse_comment, meta = meta)


			# 下一页
			# 需要登录

				


		except Exception as e:
			print 'error=====>',e
		finally:
			driver.quit()


	# 爬取回复
	# def parse_comment(self, response):
 #        comment_list = json.loads(response.body)['data']['comment_list']
 #        for value in comment_list.values():
 #            comments = value['comment_info']
 #            for comment in comments:
 #                item = CommentItem()
 #                item['id'] = comment['comment_id']
 #                item['author'] = comment['username']
 #                item['post_id'] = comment['post_id']
 #                item['content'] = helper.parse_content(comment['content'], False)
 #                item['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(comment['now_time']))
 #                yield item











		
