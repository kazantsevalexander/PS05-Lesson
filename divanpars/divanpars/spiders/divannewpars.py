import scrapy


class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def parse(self, response):
        divans = response.css('div._Ud0k')
        for divan in divans:
            yield {
                'name': divan.css('div.lsooF span::text').get(),
                'price': divan.css('div.pY3d2 span::text').get(),
                'url': f"https://www.divan.ru{divan.css('a').attrib['href']}"
            }

        # Получаем номер текущей страницы из URL
        current_page = response.url.split('-')[-1] if '-' in response.url else '1'
        next_page = int(current_page) + 1

        # Формируем URL следующей страницы
        if next_page <= 4:  # Проверяем, что не превышаем 4 страницы
            next_page_url = f"https://www.divan.ru/category/svet/page-{next_page}"
            yield scrapy.Request(next_page_url, callback=self.parse)
