import scrapy
import time

class CraigslistSpider(scrapy.Spider):
    name = 'RVs'

    start_urls = ['https://salem.craigslist.org/search/rva']

    def parse(self, response):
        page_links = response.xpath('//*[@id="search-results"]//li/a/@href')
        for link in page_links:
            time.sleep(2) #sleep time to avoid being detected as a bot
            yield response.follow(link, self.parse_page)

        pagination_links = response.xpath('//*[@class="button next"]/@href')[0]
        if not not pagination_links:
            yield response.follow(pagination_links.extract(), self.parse)
        else:
            print('**Done Scraping!!!***' * 10)

    def parse_page(self, response):
        print('**PARSING!**' * 15)
        time.sleep(2)
        yield {
            'title': response.xpath('//*[@id="titletextonly"]/text()').extract()[0],
            'url' : response.url,
            'price' : response.xpath('//*[@class="price"]/text()').extract()[0],
            'latitude' : response.xpath('//*[@id="map"]/@data-latitude').extract()[0],
            'longitude' : response.xpath('//*[@id="map"]/@data-longitude').extract()[0],
            'description' : response.xpath('//*[@id="postingbody"]/text()').extract()[1]
        }

