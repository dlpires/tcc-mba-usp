from time import sleep
import scrapy
from scrapy.loader import ItemLoader
import json
from youtube_channels.shared import utils

## SELENIUM
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException
from typing import Iterable
from scrapy.selector import Selector
from scrapy.http import Request

from youtube_channels.items import YoutubeChannelsItem

class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["www.google.com", "google.com", "www.youtube.com", "youtube.com"]
    start_urls = ["https://www.google.com"]


    def start_requests(self) -> Iterable[Request]:
        ## SET PROFILE LANGUAGE PT-BR IN BROWSER
        remote_server = "http://localhost:4444"
        options = webdriver.FirefoxOptions()
        options.set_preference('intl.accept_languages', 'pt-BR, pt')
        search_key = 'Cozinha'
        num_results = 25

        try:
            # CONNECT TO WEBDRIVER REMOTE
            # self.driver = webdriver.Remote(command_executor=remote_server, options=options)
        
            # CONNECT TO WEBDRIVER LOCAL (FIREFOX)
            self.driver = webdriver.Firefox(options=options)
            self.logger.info('Sleeping for 5 seconds.')
            sleep(5)

            self.driver.get(self.start_urls[0])
            self.logger.info('Sleeping for 5 seconds.')
            sleep(5)

            search_input = self.driver.find_element(By.NAME, 'q')
            search_input.send_keys('site:youtube.com/@ AND intext:'+search_key) #send keys for searching
            search_input.send_keys(Keys.RETURN) #ENTER
            self.logger.info('Sleeping for 5 seconds.')
            sleep(5)

            # INCLUDING THE 40TH RESULTS
            self.driver.get(self.driver.current_url+'&num='+str(num_results))
            self.logger.info('Sleeping for 3 seconds.')
            sleep(3)

            sel = Selector(text=self.driver.page_source)

            ## GET URLS LIST
            channels = sel.xpath('//a[@jsname="UWckNb"]/@href').extract()

            channels_fmt = []

            ## ADJUSTING LINKS TO ACCESS VIDEOS TAB ON CHANNELS
            for ch in channels:
                ## strings in lowercase
                ch = ch.lower()

                ## IF /VIDEOS are included, it's ready!
                if '/videos' not in ch:
                    ## CHECK LAST SUBSTRING IN STRING, IF IS THE CHANNEL NAME, INCLUDING /VIDEOS IN LINK 
                    if '@' in ch.split('/')[-1]:
                        result = ch+'/videos'
                    else:
                        result = ch.replace('/'+ch.split('/')[-1],'/videos')
                else:
                    result = ch
                
                ## IF ALREADY EXISTS, NOT INCLUDING IN ARRAY
                if [s for s in channels_fmt if ch.split('/')[3] in s] == []:
                    channels_fmt.append(result)

            # ACCESS CHANNELS TO PARSE
            for ch_url in channels_fmt:
                yield Request(ch_url, callback=self.parse_channels)

        except TimeoutException as te:
            self.logger.info('TimeoutException: ', te)
        except WebDriverException as we:
            self.logger.info('WebDriverException: ', we)
        # finally:
        #     ## CLOSE WEB BROWSER
        #     self.driver.quit()


    ## PARSE CHANNELS
    def parse_channels(self, response):
        l = ItemLoader(item=YoutubeChannelsItem(), response=response)

        ## NAVIGATE TO URL
        self.driver.get(response.request.url)
        
        self.logger.info('Sleeping for 5 seconds.')
        sleep(5)

        # INVOKE MODAL FOR MORE INFOS
        actions = ActionChains(self.driver)
        buttonMoreInfo = self.driver.find_element(By.XPATH, '//button[contains(@class, "truncated-text-wiz__")]')
        actions.move_to_element(buttonMoreInfo)
        actions.click(buttonMoreInfo)
        actions.perform()
        self.logger.info('Sleeping for 3 seconds.')
        sleep(3)

        sel = Selector(text=self.driver.page_source)

        self.logger.info('Sleeping for 3 seconds.')
        sleep(3)

        ## GET INFORMATION
        channel_name = sel.xpath('//meta[@itemprop = "name"]/@content').extract_first()
        channel_account = self.driver.current_url.split('/')[3]
        channel_url = self.driver.current_url
        
        subscribers = sel.xpath('//span/text()[contains(.,"inscritos")]').extract_first()
        subscribers = utils.normalizeString(subscribers)
        subscribers = utils.extractNumber(',', subscribers)
        
        num_videos = sel.xpath('//span/text()[contains(.,"vídeos")]').extract_first()
        num_videos = utils.normalizeString(num_videos)
        num_videos = utils.extractNumber(',', num_videos)

        num_views = sel.xpath('//td/text()[contains(.,"visualizações")]').extract_first()
        num_views = utils.extractNumber('.', num_views)

        keywords = sel.xpath('//meta[@property="og:video:tag"]/@content').extract()

        l.add_value('channel_name', channel_name)
        l.add_value('channel_account', channel_account)
        l.add_value('channel_url', channel_url)
        l.add_value('subscribers', subscribers)
        l.add_value('num_videos', num_videos)
        l.add_value('num_views', num_views)
        l.add_value('keywords', keywords)

        yield l.load_item()

    def parse(self, response):
        pass
