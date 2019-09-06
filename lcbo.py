import scrapy

page_num = 0

class lcboSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15?pageView=grid&orderBy=3&fromPage=catalogEntryList&beginIndex=' + str(page_num),
    ]


    def parse(self, response):
        for quote in response.css('.product_price'):
            yield {
                'price': quote.css('span.price ::text').get().strip(),
            }

        next_page = 'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/spirits-15?pageView=grid&orderBy=3&fromPage=catalogEntryList&beginIndex=' + str(page_num + 12)
        if next_page is not None:
            yield response.follow(next_page, self.parse)
