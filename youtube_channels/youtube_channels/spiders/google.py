import scrapy
import json

## SELENIUM
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException
from typing import Iterable
from scrapy.selector import Selector
from scrapy.http import Request
from time import sleep


class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["www.google.com", "google.com"]
    start_urls = ["https://www.google.com"]


    def start_requests(self) -> Iterable[Request]:
        ## SET PROFILE LANGUAGE PT-BR IN BROWSER
        remote_server = "http://localhost:4444"
        options = webdriver.FirefoxOptions()
        options.set_preference('intl.accept_languages', 'pt-BR, pt')
        search_key = 'Biologia'
        num_results = 40

        try:
            #self.driver = webdriver.Firefox(options=options)
            ## CONNECT TO WEBDRIVER REMOTE
            # self.driver = webdriver.Remote(command_executor=remote_server, options=options)
        
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

            sel = Selector(text=self.driver.page_source)
            self.logger.info('Sleeping for 3 seconds.')
            sleep(3)

            ## GET URLS LIST
            channels = sel.xpath('//a[@jsname="UWckNb"]/@href').extract()

            print(json.dumps(channels, indent = 4))

            yield "success!"

        except TimeoutException as timeouterr:
            self.logger.info('TimeoutException: ', timeouterr)
        except WebDriverException as webdrivererr:
            self.logger.info('WebDriverException: ', webdrivererr)
        finally:
            ## CLOSE WEB BROWSER
            self.driver.quit()

    def parse(self, response):
        pass
