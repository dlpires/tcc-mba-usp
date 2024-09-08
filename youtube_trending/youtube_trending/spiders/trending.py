from time import sleep
from scrapy import Spider
from scrapy.loader import ItemLoader
import os
import glob
import json
import youtube_trending.shared.utils as utils

# SELENIUM
from typing import Iterable
from scrapy.selector import Selector
from scrapy.http import Request
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException

##
from youtube_trending.items import YoutubeTrendingItem

class TrendingSpider(Spider):
    name = "trending"
    allowed_domains = ["www.youtube.com","youtube.com"]
    start_urls = ["https://www.youtube.com/feed/trending"]
    base_url = "https://www.youtube.com"
    
    def start_requests(self) -> Iterable[Request]:
        ## SET PROFILE LANGUAGE PT-BR IN BROWSER
        remote_server = "http://localhost:4444"
        options = webdriver.FirefoxOptions()
        options.set_preference('intl.accept_languages', 'pt-BR, pt')

        try:
            #self.driver = webdriver.Firefox(options=options)
            ## CONNECT TO WEBDRIVER REMOTE
            self.driver = webdriver.Remote(command_executor=remote_server, options=options)
            self.logger.info('Sleeping for 5 seconds.')
            sleep(5)
            self.driver.get(self.start_urls[0])

            sel = Selector(text=self.driver.page_source)
            self.logger.info('Sleeping for 3 seconds.')
            sleep(3)
            videos = sel.xpath('//a[@id="thumbnail"]/@href').extract()

            for video in videos:
                url = self.base_url + video
                # EXCLUDING SHORTS
                if ("shorts" not in url):
                    yield Request(url, callback=self.parse_trendings)
        except TimeoutException as timeouterr:
            self.logger.info('TimeoutException: ', timeouterr)
        except WebDriverException as webdrivererr:
            self.logger.info('WebDriverException: ', webdrivererr)
        # finally:
        #     ## CLOSE WEB BROWSER
        #     self.driver.quit()

    def parse_trendings(self, response):
        l = ItemLoader(item=YoutubeTrendingItem(), response=response)
        
        ## NAVIGATE TO URL
        self.driver.get(response.request.url)
        self.logger.info('Sleeping for 3 seconds.')
        sleep(3)

        ## SCROLL DOWN TO COMMENTS INFO TO LOAD
        self.driver.execute_script("javascript:window.scrollBy(50, 500)")

        self.logger.info('Sleeping for 5 seconds.')
        sleep(5)
        
        ## GET HTML PAGE
        sel = Selector(text=self.driver.page_source)
        self.logger.info('Sleeping for 3 seconds.')
        sleep(3)
        
        video_name = sel.xpath('//yt-formatted-string/text()').extract_first()
        video_channel_name = sel.xpath('//ytd-channel-name/div/div/yt-formatted-string/a/text()').extract_first()
        ch_ac_temp = sel.xpath('//yt-formatted-string/a/@href').extract_first()
        video_channel_account = ch_ac_temp.split('/')[1] if ch_ac_temp.split('/')[1] != 'channel' else None
        video_url = self.driver.current_url

        likes = sel.xpath('//like-button-view-model/toggle-button-view-model/button-view-model/button/@aria-label').extract_first()
        ## extract likes
        likes = utils.extractNumber(likes)
        
        others = sel.xpath('//ytd-watch-info-text/tp-yt-paper-tooltip/div/text()').extract_first().split()
        
        views = utils.extractNumber(others[0])
        
        ranking_date = str(utils.getDateNow()) # GET EXECUTION CRAWLER DATE

        for x in others:
            if(utils.checkRanking(x) != None):
                rank_trend = x
                break
            else:
                rank_trend = None

        comments_tmp = sel.xpath('//yt-formatted-string[contains(@class, "ytd-comments-header-renderer")]/span/text()').extract_first()
        
        if (comments_tmp != None):
            comments = utils.extractNumber(comments_tmp)
        else:
            comments = None

        ## GET KEYWORDS CHANNEL
        self.driver.get(self.base_url + ch_ac_temp)
        self.logger.info('Sleeping for 3 seconds.')
        sleep(3)

        sel = Selector(text=self.driver.page_source)
        
        ## IF CHANNEL ACCOUNT VARIABLE RECEIVE NONE (NOT HAVE ACCOUNT INFO), GET INFO IN CHANNEL
        if not video_channel_account:
            video_channel_account = sel.xpath('//yt-content-metadata-view-model/div/span/text()').extract_first()

        keywords = sel.xpath('//meta[@property="og:video:tag"]/@content').extract()

        l.add_value('video_name', video_name)
        l.add_value('video_channel_name', video_channel_name)
        l.add_value('video_channel_account', video_channel_account)
        l.add_value('video_url', video_url)
        l.add_value('rank_trend', rank_trend)
        l.add_value('likes', likes)
        l.add_value('views', views)
        l.add_value('comments', comments)
        l.add_value('ranking_date', ranking_date)
        l.add_value('keywords', keywords)

        yield l.load_item()

    def close(self, reason):
        ## CLOSE WEB BROWSER
        self.driver.quit()
        # json_file = max(glob.iglob('*.json'), key=os.path.getctime)
        # os.rename(json_file, "trendings.json")