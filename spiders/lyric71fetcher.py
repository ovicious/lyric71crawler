# -*- coding: utf-8 -*-
import scrapy
from ..items import Lyric71Item


class Lyric71fetcherSpider(scrapy.Spider):
    name = 'lyric71fetcher'
    #allowed_domains = ['lyric71.net']
    start_urls = ['http://lyrics71.net/']

    def parse(self,response):
        links = response.xpath('//*[@id="artists-collapse"]/div/div/ul/li[*]/a/@href').extract()
        print(links)
        for link in links:
            yield scrapy.Request(link,callback=self.parse_infos)
        

    def parse_infos(self,response):
        
        #request = scrapy.Request(Lyric71fetcherSpider.parse.link,callback=parse_lyrics)
        #title = response.css('.col-xs-6 a::text').extract()
        #artist = response.css('.col-xs-3+ .col-xs-3 a::text').extract()
        #album = response.css('.col-xs-6+ .col-xs-3 a::text').extract()
        #print(title,artist,album)
        #yield {
        #    'title': title,
        #    'artist' : artist,
        #    'album' : album
        #}
        
        lyric_links = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "col-xs-6", " " ))]//a/@href').extract()
        for lyr_link in lyric_links:
            yield scrapy.Request(lyr_link,callback=self.parse_lyrics)

    def parse_lyrics(self,response):
        items = Lyric71Item()
        lyric = response.css('p+ p::text').extract()
        info = response.css('strong::text').extract()
        #artist = Lyric71fetcherSpider.parse_infos(artist)
        #album = parse_infos(album)
        #title = parse_infos(title)
        #print(lyric)
        #print(info)
        yield {
           'info':info,
            #'artist' : artist,
            #'album'  : album,
            #'track'  : title,
            'lyric'  : lyric
        }
