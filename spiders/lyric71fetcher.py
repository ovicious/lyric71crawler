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
        print('')
        #request = scrapy.Request(Lyric71fetcherSpider.parse.link,callback=parse_lyrics)
        #title = scrapy.response.css('.col-xs-6 a::text').extract()
        #artist = response.css('.col-xs-3+ .col-xs-3 a::text').extract()
        #album = response.css('.col-xs-6+ .col-xs-3 a::text').extract()
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
        info = response.css('a+ p::text').extract()
        print(lyric)
        print(info)
        yield items

'''
    def start_requests(self):
        title = response.css('.col-xs-6 a::text').extract()
        artist = response.css('.col-xs-3+ .col-xs-3 a::text').extract()
        album = response.css('.col-xs-6+ .col-xs-3 a::text').extract()
        yield {
            'title': title,
            'artist' : artist,
            'album' : album }
        yield scrapy.Request("",callback=parse_page1)
        item = MyItem()
    def parse_infos(self, response):
        item['main_url'] = response.url ##extracts http://www.example.com/main_page.html
        request = scrapy.Request("http://www.example.com/some_page.html",callback=self.parse_page2)
        request.meta['my_meta_item'] = item ## passing item in the meta dictionary
        ##alternatively you can follow as below
        ##request = scrapy.Request("http://www.example.com/some_page.html",meta={'my_meta_item':item},callback=self.parse_page2)
        return request

    def parse_lyrics(self, response):
        item = response.meta['my_meta_item']
        item['other_url'] = response.url ##extracts http://www.example.com/some_page.html
        return item

        '''