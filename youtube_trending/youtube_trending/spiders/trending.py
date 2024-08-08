from scrapy import Spider
from scrapy.loader import ItemLoader
import os
import glob
import json
import youtube_trending.shared.utils as utils

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
    remove_strings = ['Transmitido','ao','vivo','em']
    
    def start_requests(self) -> Iterable[Request]:
        ## SET PROFILE LANGUAGE PT-BR IN BROWSER
        options = webdriver.FirefoxOptions()
        options.set_preference('intl.accept_languages', 'pt-BR, pt')

        self.driver = webdriver.Firefox(options=options)
        self.logger.info('Sleeping for 5 seconds.')
        sleep(5)
        self.driver.get(self.start_urls[0])

        sel = Selector(text=self.driver.page_source)
        self.logger.info('Sleeping for 3 seconds.')
        sleep(3)
        videos = sel.xpath('//a[@id="thumbnail"]/@href').extract()

        # yield {"videos": videos}

        for video in videos:
            url = self.base_url + video
            # EXCLUDING SHORTS
            if ("shorts" not in url):
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
        self.driver.get(response.request.url)
        self.logger.info('Sleeping for 5 seconds.')
        sleep(5)
        sel = Selector(text=self.driver.page_source)
        self.logger.info('Sleeping for 3 seconds.')
        sleep(3)
        video_name = sel.xpath('//yt-formatted-string/text()').extract_first()
        video_channel_name = sel.xpath('//ytd-channel-name/div/div/yt-formatted-string/a/text()').extract_first()
        video_url = self.driver.current_url

        likes = sel.xpath('//like-button-view-model/toggle-button-view-model/button-view-model/button/@aria-label').extract_first()
        ## extract likes
        likes = utils.extractNumber(likes)
        
        others = sel.xpath('//ytd-watch-info-text/tp-yt-paper-tooltip/div/text()').extract_first().split()
        ## REMOVE UNECESSARY VALUES
        if (True in [y in others for y in self.remove_strings]):
            [others.remove(x) for x in self.remove_strings]
        
        views = utils.extractNumber(others[0])
        
        dt_fmt = "%d de %b. de %Y"
        dt_str = ' '.join(others[3:8])
        upload_time = utils.extractDate(dt_str, dt_fmt)

        rank_trend = others[9]
        
        comments = sel.xpath('//div/h2[contains(@aria-label, "Com")]/@aria-label').extract_first()
        ## extract comments
        comments = utils.extractNumber(comments)

        self.logger.info('Sleeping for 5 seconds.')
        sleep(5)

        yield {
            "video_name": video_name,
            "video_channel_name": video_channel_name,
            "video_url": video_url,
            "rank_trend": rank_trend,
            "likes": likes,
            "views": views,
            "comments": comments,
            "upload_time": upload_time
        }
    
    def parse(self, response):
        pass
    
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