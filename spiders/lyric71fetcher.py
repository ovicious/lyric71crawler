# -*- coding: utf-8 -*-
import scrapy
import w3lib.html
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
        lyric_whole = response.css('p+ p::text').extract()
        
        # Whole lyric as one json value with /n tag
        lyric_joined=str(" ".join(lyric_whole))
        #lyric = lyric_joined # with \n tag
        lyric = lyric_joined.replace("\n","") # without \n tags
        
        all_info = response.css('strong::text').extract()
        for infu in all_info:
            if 'কন্ঠঃ' in str(infu):
                artist=infu.replace("\nকন্ঠঃ ","")
            else:
                aritst=''
            #if 'শিরোনামঃ' in str(infu):
            #    title=infu.replace("\nশিরোনামঃ ","")[1]
            #else:
            #    title=''
            if 'অ্যালবামঃ' in str(infu):
                album=infu.replace('\nঅ্যালবামঃ ',"")
            else:
                album=''
               
        #info = response.css('strong::text').extract_first().split('শিরোনামঃ ')[1]
        title = response.css('strong::text').extract_first().replace("শিরোনামঃ ","")
        
        
        yield {
        #   'info':info,
           'artist':artist,
          'album':album,
            'title':title,
            'lyric':lyric
        }



        