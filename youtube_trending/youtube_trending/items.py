# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YoutubeTrendingItem(scrapy.Item):
    # define the fields for your item here like:
    video_name = scrapy.Field()
    video_channel_name = scrapy.Field()
    video_channel_account = scrapy.Field()
    video_url = scrapy.Field()
    likes = scrapy.Field()
    views = scrapy.Field()
    comments = scrapy.Field()
    ranking_date = scrapy.Field()
    rank_trend = scrapy.Field()
    keywords = scrapy.Field()
