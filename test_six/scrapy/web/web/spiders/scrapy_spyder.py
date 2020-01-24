import scrapy

class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)

class  crawl(scrapy.Spider):
    name="products"

    start_url=[
        'https://www.woolworths.com.au/shop/browse/drinks/cordials-juices-iced-teas/iced-teas',
    ]

    def parse(self, response):
        for product in response.css('div.shelfProductTitle-content'):
            yield {
                Product['name']: product.css('div.h3.a::text').getall(),

            }

