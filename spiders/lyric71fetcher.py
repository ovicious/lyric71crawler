# -*- coding: utf-8 -*-
import scrapy
from ..items import Lyric71Item


class Lyric71fetcherSpider(scrapy.Spider):
    name = 'lyric71fetcher'

    start_urls = ['http://lyrics71.net/all-lyrics/']
    total_tracks=0

    def parse(self,response):
        links = response.xpath('//*[@id="wrapper"]/div[2]/div/div[1]/div/div/div[3]/ul/li[*]/a[2]/@href').extract()
        for link in links:
            yield scrapy.Request(link,callback=self.parse_lyrics)
        

    def parse_lyrics(self,response):
        Lyric71fetcherSpider.total_tracks +=1
        print(Lyric71fetcherSpider.total_tracks)
        items = Lyric71Item()
        lyric = response.css('p+ p::text').extract()
        info = response.css('strong::text').extract()
        print (info)
        yield {
           'info':info,
        #    'artist' : artist,
        #    'album'  : album,
        #    'track'  : title,
            'lyric':lyric
        }



        