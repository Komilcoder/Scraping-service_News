import scrapy


class ReutersSpider(scrapy.Spider):
    name = 'reuters'
    allowed_domains = ['kun.uz']
    start_urls = ['https://kun.uz/en/news/category/politics']

    def parse(self, response):
        print("parse", response)
        print(response.xpath("//a[@class='menu-link']"), "sadasdsddddddd")
        news = response.xpath("//div[@class='wrapper']")
        print(news, "ooooooooooooooooo")
        for new in news:
            title = new.xpath("//span[@class='big-news__title']").get()
            description = new.xpath("//span[@class='big-news__description']").get()
            news_info = {
                "title": title,
                "description": description
            }
            yield news_info
            # if news_info:
            #     absl_url = f"https://kun.uz{news_info}"
            #     yield scrapy.Request(url=absl_url, callback=self.parse)
