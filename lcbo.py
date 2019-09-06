import scrapy
import re

class LcboSpider(scrapy.Spider):
    name = "lcboscrape"
    start_urls = ['https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15?pageView=grid&orderBy=3&fromPage=catalogEntryList&beginIndex=0']

    def parse(self, response):
        urls = response.css('.product_name a').xpath('@href').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, cookies={'WC_physicalStoreAddress':'YONGE\%20\%26\%20SHEPPARD'}, callback=self.parse_details)

        next_page_url = response.css('.right_arrow').xpath('@href').get()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        info = re.findall(r'<span>(.*?)</span>', response.css('.product-details-list').get())
        size = ''.join(info).rsplit('mL',1)[0].strip()
        alcohol = ''.join(filter(lambda x: '%' in x, info)[0]).replace("%","")
        image = response.css('.product_main_image').xpath('@src').get()
        # available = response.css('.walkInDetails ::text').get().strip().rsplit('<div>',1)
        yield {
            'name': response.css('h1.main_header ::text').get().strip(),
            'price': float(response.css('.price ::text').get().strip().replace("$","")),
            'size': int(re.sub("\D", "", size)),
            'alcohol': int(alcohol),
            'image': image,
            # 'available': available,
        }
