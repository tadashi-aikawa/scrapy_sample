from urllib.parse import urljoin

import scrapy
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=+9), "JST")


class BlogSpider(scrapy.Spider):
    name = "blog"
    allowed_domains = ["blog.mamansoft.net"]
    start_urls = ["https://blog.mamansoft.net/"]

    def parse(self, response, **kwargs):
        need_not_next = False

        for article in response.css("article"):
            title = article.css("h1 > a::text").get().strip()
            _datetime = article.css("time::attr(datetime)").get()
            url = article.css("a::attr(href)").get()

            if datetime.fromisoformat(_datetime) < datetime(2020, 12, 1, tzinfo=JST):
                need_not_next = True
                continue

            yield response.follow(
                url, self.parse_page, cb_kwargs={"title": title, "_datetime": _datetime}
            )

        if need_not_next:
            return True

        next_url = response.css(".pagination-next > a::attr(href)").get()
        if next_url:
            yield response.follow(next_url, self.parse)

    def parse_page(self, response, title, _datetime):
        tags = response.css(".post-footer-tags > a.tag::text").getall()
        image_url = response.css(".cover-image > img::attr(src)").get()

        yield {
            "title": title,
            "datetime": _datetime,
            "tags": tags,
            "image_urls": [urljoin(response.url, image_url)] if image_url else [],
        }
