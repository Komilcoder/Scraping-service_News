import scrapy
from ..items import ScrapynewsItem
from scrapy.loader import ItemLoader
from scrapy.utils.defer import maybe_deferred_to_future
from twisted.internet.defer import DeferredList
from scrapy import Request


class ReutersSpider(scrapy.Spider):
    name = 'reuters'
    allowed_domains = ['kun.uz']
    start_urls = ['https://kun.uz/en/news/category/society']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    async def parse(self, response):

        news = response.css('div#news-list')
        parent_div = response.xpath('//div[@id="news-list"]')

        child_div = parent_div.xpath('//div[@class="news"]')
        a_tags = child_div.xpath('.//a')

        description = response.xpath('//div[@class="single-layout__center slc"]')
        additional_request = Request("https://kun.uz/en/news/")
        deferred = self.crawler.engine.download(additional_request)
        additional_response = await maybe_deferred_to_future(deferred)
        x = additional_response.css('div.single-layout__center slc').get()
        print(x, "wwwwwwwwwwwwwwwww")

        for a_tag in a_tags:
            title = a_tag.xpath('text()').extract_first()

            news = {"title": title, 'description': additional_response.css('div.single-layout__center slc '
                                                                           'div.single-content').get(), }
            if title is not None and additional_response is not None:
                yield news
        load_more_button = response.xpath('//div[@class="top-news"]')
        for load in load_more_button:
            more_button = load.css('div.load-more a.load-more__link').attrib['href']
            if more_button is not None:
                yield response.follow(more_button, callback=self.parse)


