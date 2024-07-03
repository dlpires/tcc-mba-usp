from scrapy import Spider
from scrapy.loader import ItemLoader
import os
import glob
import json

# SELENIUM
from time import sleep
from typing import Any, Iterable
from scrapy.selector import Selector
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

##
from youtube_trending.items import YoutubeTrendingItem


class TrendingSpider(Spider):
    name = "trending"
    allowed_domains = ["www.youtube.com","youtube.com"]
    start_urls = ["https://www.youtube.com/feed/trending"]
    base_url = "https://www.youtube.com"
    
    def start_requests(self) -> Iterable[Request]:
        self.driver = webdriver.Firefox()
        self.driver.get(self.start_urls[0])

        sel = Selector(text=self.driver.page_source)
        sleep(3)
        self.logger.info('Sleeping for 3 seconds.')
        videos = sel.xpath('//a[@id="thumbnail"]/@href').extract()

        # yield {"videos": videos}

        for video in videos:
            url = self.base_url + video
            yield Request(url, callback=self.parse_trendings)
        
        # while True:
        #     try:
        #         next_page = self.driver.find_element(By.XPATH, '//a[text()="next"]')
        #         sleep(3)
        #         self.logger.info('Sleeping for 3 seconds.')
        #         next_page.click()

        #         sel = Selector(text=self.driver.page_source)
        #         books = sel.xpath('//h3/a/@href').extract()
                
        #         for book in books:
        #             url = 'https://books.toscrape.com/'+book
        #             yield Request(url, callback=self.parse_book)
        #     except NoSuchElementException:
        #         self.logger.info('No more pages to load.')
        #         self.driver.quit()
        #         break

    def parse_trendings(self, response):
        sel = Selector(text=self.driver.page_source)
        video_name = sel.xpath('//yt-formatted-string/text()').extract_first()

        yield {"video_name": video_name}
    
    
    # def parse(self, response):
    #     l = ItemLoader(item=YoutubeTrendingItem(), response=response)

    #     # video_name = response.xpath('//yt-formatted-string/text()').extract()
    #     #video_channel_name = response.xpath('//*[@class="tag-item"]/a/text()').extract()
    #     #views = response.xpath('//*[@class="tag-item"]/a/text()').extract()
    #     #upload_time = response.xpath('//*[@class="tag-item"]/a/text()').extract()

    #     l.add_value('video_name', video_name)
    #     #l.add_value('video_channel_name', video_channel_name)
    #     #l.add_value('views', views)
    #     #l.add_value('upload_time', upload_time)


    #     yield l.load_item()
        

    # def close(self, reason):
    #     json_file = max(glob.iglob('*.json'), key=os.path.getctime)
    #     os.rename(json_file, "trendings.json")