# -*- coding: utf-8 -*-
import scrapy


class Lyric71fetcherSpider(scrapy.Spider):
    name = 'lyric71fetcher'
    #allowed_domains = ['lyric71.net']
    start_urls = ['https://lyrics71.net/alphabetic-lyrics-list/?letter=num']

    def parse(self, response):
        title = response.css('.col-xs-6 a::text').extract()
        artist = response.css('.col-xs-3+ .col-xs-3 a::text').extract()

        yield {
            'title': title,
            'artist' : artist
        }
