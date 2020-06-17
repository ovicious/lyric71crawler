# -*- coding: utf-8 -*-
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from w3lib.html import remove_tags
from bs4 import BeautifulSoup
from ..items import Lyric71Item



class Lyric71fetcherSpider(scrapy.Spider):
    name = 'lyric71fetcher'

    start_urls = ['http://lyrics71.net/all-lyrics/']
    total_tracks=0

    def parse(self,response):
        links = response.xpath('//*[@id="wrapper"]/div[2]/div/div[1]/div/div/div[3]/ul/li[*]/a[2]/@href').extract()
        for link in links:
            yield scrapy.Request(link,callback=self.parse_lyrics,errback=self.errback_httpbin,
                                    dont_filter=True)
        
    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

    def parse_lyrics(self,response):
        Lyric71fetcherSpider.total_tracks +=1
        print(Lyric71fetcherSpider.total_tracks)
        items = Lyric71Item()
        artist=''
        album =''
        movie= ''
        drama=''
        composer =''
        writer = ''
        #splited =''
        lyric_whole = response.css('p+ p::text').extract()
        
        # Whole lyric as one json value with /n tag
        lyric_joined=str(" ".join(lyric_whole))
        #lyric = lyric_joined # with \n tag
        lyric = lyric_joined.replace("\n","") # without \n tags
        
        whole_info = response.xpath('//strong').extract()[0] 
        removed_tags = BeautifulSoup(str(whole_info), "lxml").text
        splited = removed_tags.split("\n")
        
      
        for elem in (splited):
        
            if 'শিরোনামঃ' in str(elem):
            
                title = elem.replace('শিরোনামঃ','')
                print (title)
            #else:
            #    title = ''     

            if 'কন্ঠঃ' in elem:
            
                artist = elem.replace('কন্ঠঃ','') 
            #else:
            #    artist = ''

            if 'সুরঃ' in elem:
            
                composer = elem.replace('সুরঃ','') 
            #else:
            #    composer = ''    

            if 'কথাঃ' in elem:
            
                writer = elem.replace('কথাঃ','') 
            #else:
            #    writer = ''
            if 'অ্যালবামঃ' in elem:
            
                album = elem.replace('অ্যালবামঃ','') 
            #else:
            #    album = ''
            if 'অ্যালবামঃ' in elem:
            
                album = elem.replace('অ্যালবামঃ','') 
            #else:
            #    album = ''
            if 'ব্যান্ডঃ' in elem:
            
                band = elem.replace('ব্যান্ডঃ','') 
            #else:
            #    band = ''
            if 'মুভিঃ' in elem:
            
                movie = elem.replace('মুভিঃ','') 
            #else:
            #    movie = ''
            if 'নাটকঃ' in elem:
            
                drama = elem.replace('নাটকঃ','') 
            #else:
            #    drama = ''
            #else:
        yield {
            'artist' : artist,
            'album'  : album,
            'title'  : title,
            'writer' : writer,
            'movie'  : movie,
            'drama'  : drama,
            'lyric'  : lyric
                }

'''  

# 'শিরোনামঃ খোকা\nকন্ঠঃ প্রীতম হাসান, ফেরদৌস ওয়াহিদ\nকথাঃ প্রীতম হাসান, নুহাশ হুমায়ুন\nসুরঃ প্রীতম হাসান'

# whole_info = response.xpath('//strong')
## [<Selector xpath='//strong' data='<strong>শিরোনামঃ খোকা<br>\nকন্ঠঃ প্রীত...'>,
 <Selector xpath='//strong' data='<strong>শিরোনামঃ খোকা<br>\nকন্ঠঃ প্রীত...'>] 

### start
 # whole_info = response.xpath('//strong').extract()[0]
 ## ['<strong>শিরোনামঃ খোকা<br>\nকন্ঠঃ প্রীতম হাসান, ফেরদৌস ওয়াহিদ<br>\nকথাঃ প্রীতম হাসান, নুহাশ হুমায়ুন<br>\nসুরঃ প্রীতম হাসান</strong>']

# removed_tags = BeautifulSoup(str(whole_info), "lxml").text
'শিরোনামঃ খোকা\nকন্ঠঃ প্রীতম হাসান, ফেরদৌস ওয়াহিদ\nকথাঃ প্রীতম হাসান, নুহাশ হুমায়ুন\nসুরঃ প্রীতম হাসান'[--[-]]

# splited = removed_tags.split("\n")
### ['শিরোনামঃ খোকা',
 'কন্ঠঃ প্রীতম হাসান, ফেরদৌস ওয়াহিদ',
 'কথাঃ প্রীতম হাসান, নুহাশ হুমায়ুন',
 'সুরঃ প্রীতম হাসান']

for elem in splited:

    if 'শিরোনামঃ' in elem:
 
        title = elem.replace('শিরোনামঃ','')
        print(title) 
    else:
        title = ''     
        print(title)
    if 'কন্ঠঃ' in elem:
 
        artist = elem.replace('কন্ঠঃ','') 
        print(artist)
    else:
        artist = ''
        print(artist)
    if 'সুরঃ' in elem:
 
        composer = elem.replace('সুরঃ','') 
        print(composer)
    else:
        composer = ''    
        print(composer)
    if 'কথাঃ' in elem:
 
        writer = elem.replace('কথাঃ','') 
        print(writer)
    else:
        writer = ''
        print(writer)
    if 'অ্যালবামঃ' in elem:
 
        album = elem.replace('অ্যালবামঃ','') 
        print(album)
    else:
        album = ''
        print(album)
    if 'ব্যান্ডঃ' in elem:
 
        band = elem.replace('ব্যান্ডঃ','') 
    else:
        band = ''
    if 'মুভিঃ' in elem:
 
        movie = elem.replace('মুভিঃ','') 
    else:
        movie = ''
    if 'নাটকঃ' in elem:
 
        drama = elem.replace('নাটকঃ','') 
    else:
        drama = ''

        
['শিরোনামঃ আমার প্রান ধরিয়া মারো টান',
 'কথাঃ অতনু তিয়াস',
 'সুরঃ ইমন চৌধুরী',
 'কন্ঠঃ ইমন চৌধুরী',
 'নাটকঃ আবার তোরা সাহেব হ']
        

        
        
        '''