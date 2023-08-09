import os 

# Import logging => Library used for logs manipulation 
## More info => https://docs.python.org/3/library/logging.html
import logging

# Import scrapy and scrapy.crawler 
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import re

# Collect name of different cities
booking_cities_df = pd.read_csv('weather_df.csv')


#This is a Scrapy spider class responsible for defining the behavior of the spider.
class BookingHotelInfo(scrapy.Spider):
    
    name = "booking"

    cities = booking_cities_df['cities']
    pages = ['0', '35', '70']


    start_urls = [

        #'https://www.booking.com/searchresults.html?'+'offset={}'.format(i) for i in [0, 35, 70]
        'https://www.booking.com/searchresults.html?'
        
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 2, # 2 seconds of delay
        'RANDOMIZE_DOWNLOAD_DELAY': True, # By default, when you set DOWNLOAD_DELAY = 2 for example, Scrapy will introduce random delays of between: 
                                          # Lower Limit: 0.5 * DOWNLOAD_DELAY
                                          # Upper Limit: 1.5 * DOWNLOAD_DELAY
        }
    
    #The main parsing method that extracts data from search results.
    def parse(self, response):
        
        
        for city in self.cities:
            for page in self.pages:
                yield scrapy.FormRequest.from_response(
                    response,
                    formdata={'ss' : city, 'offset': page},
                    callback = self.after_search
                )

    #Method that extracts links to hotel pages from search results.
    def after_search(self, response): 

        link_url = response.css('div.dd023375f5 h3.a4225678b2 a::attr(href)').getall()

        city = response.url.split("ss=")[-1].split("&")[0],
      

        for link in link_url:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_link, meta={'city': city})
            
            
    #Method that extracts detailed information from hotel pages.
    def parse_link(self, response):

        yield{
            'city' : response.meta['city'][0].replace('+', ' '),
            'address': response.css('p#showMap2 span.hp_address_subtitle::text').get(),
            'lat_long' : response.css('p#showMap2 a::attr(data-atlas-latlng)').get(),            
            'name': response.css('h2.d2fee87262::text').get(),
            'url': response.url,
            'score' : response.css('div.a1b3f50dcd div.b5cd09854e::text').get(),
            'text_description' : response.css('div#property_description_content p::text').getall(),
                

            }
          


# Name of the file where the results will be saved
filename = "hotel_booking.json"

# If file already exists, delete it before crawling (because Scrapy will 
# concatenate the last and new results otherwise)
if filename in os.listdir('src/'):
        os.remove('src/' + filename)

# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log 
## FEEDS => Where the file will be stored 
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'src/' + filename : {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(BookingHotelInfo)
process.start()