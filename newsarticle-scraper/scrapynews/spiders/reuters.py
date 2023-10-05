import scrapy
from ..items import ScrapynewsItem
from scrapy.loader import ItemLoader
from scrapy.utils.defer import maybe_deferred_to_future
from twisted.internet.defer import DeferredList
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin
import re


class ReutersSpider(scrapy.Spider):
    name = 'reuters'
    allowed_domains = ['kun.uz']
    start_urls = ['https://kun.uz/en/news/category/society', 'https://kun.uz/en/news/category/politics',
                  'https://kun.uz/en/news/category/business', 'https://kun.uz/en/news/category/tech',
                  'https://kun.uz/en/news/category/culture', 'https://kun.uz/en/news/category/sport-en',
                  'https://kun.uz/en/news/category/tourism']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    async def parse(self, response):
        parent_div = response.xpath('//div[@id="news-list"]')
        child_div = parent_div.xpath('//div[@class="news"]')
        a_tags = child_div.xpath('.//a')

        content = response.css('span.text-uppercase::text').extract_first()

        for a_tag in a_tags:
            item = ScrapynewsItem()
            title = a_tag.xpath('text()').extract_first()
            title_url = a_tag.css('a::attr(href)').get()

            item['title'] = title
            item['url'] = "https://kun.uz" + title_url
            item['classification'] = content
            if title is not None:
                yield item
        load_more_button = response.xpath('//div[@class="top-news"]')
        for load in load_more_button:
            more_button = load.css('div.load-more a.load-more__link').attrib['href']
            if more_button is not None:
                yield response.follow(more_button, callback=self.parse)

