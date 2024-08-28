# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YoutubeChannelsItem(scrapy.Item):
    # define the fields for your item here like:
    channel_name = scrapy.Field()
    channel_account = scrapy.Field()
    channel_url = scrapy.Field()
    subscribers = scrapy.Field()
    num_videos = scrapy.Field()
    num_views = scrapy.Field()
    last_avg_likes = scrapy.Field() # LAST videos average likes
    last_avg_views = scrapy.Field() # LAST videos average views
    last_avg_comments = scrapy.Field() # LAST videos average comments
    keywords = scrapy.Field()