import scrapy

class PostSpider(scrapy.Spider):
    name = "post_spider"

    def __init__(self, start_url=None, **kwargs):
        super().__init__(**kwargs)
        self.start_url = start_url
        self.items = []

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse)

    def parse(self, response):
        item = {
            "url": response.url,
            "status": response.status,
            "body": response.body
        }
        self.items.append(item)
        yield item
