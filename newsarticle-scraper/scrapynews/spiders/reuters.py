import scrapy
from ..items import ScrapynewsItem
from scrapy.loader import ItemLoader


class ReutersSpider(scrapy.Spider):
    name = 'reuters'
    allowed_domains = ['kun.uz']
    start_urls = ['https://kun.uz/en/news/category/society']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        news = response.css('div#news-list')
        parent_div = response.xpath('//div[@id="news-list"]')

        child_div = parent_div.xpath('//div[@class="news"]')
        a_tags = child_div.xpath('.//a')

        for a_tag in a_tags:
            href = a_tag.xpath('@href').extract_first()
            title = a_tag.xpath('text()').extract_first()

        load_more_button = response.xpath('//div[@id="ias_trigger_1696323690503"]')
        more_button = load_more_button.xpath('//div[@class="load-more__link"]')
        if more_button:
            yield scrapy.FormRequest.from_response(response, formdata={'button_id': 'ias_trigger_1696323690503'}, callback=self.parse)



        # for new in news:
        #     title = new.xpath("//span[@class='big-news__title']").get()
        #     description = new.xpath("//span[@class='big-news__description']").get()
        #     news_info = {
        #         "title": title,
        #         "description": description
        #     }
        #     yield news_info
