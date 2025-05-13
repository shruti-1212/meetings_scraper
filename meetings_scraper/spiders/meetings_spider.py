import scrapy

class MeetingsSpider(scrapy.Spider):
    name = "meetings"
    start_urls = ["https://symonsrec.com/info/minutes/"]

    def parse(self, response):
        for row in response.xpath("//table/tbody/tr"):
            date = row.xpath("./td[1]/text()").get()
            meeting_title = row.xpath("./td[2]/text()").get()
            category_link = row.xpath("./td[3]/a")
            
            if category_link:
                category = category_link.xpath("text()").get()
                url = category_link.xpath("@href").get()
            else:
                category = "other"
                url = None

            yield {
                "date": date.strip() if date else None,
                "meeting_title": meeting_title.strip() if meeting_title else None,
                "category": category.strip() if category else None,
                "URL": response.urljoin(url) if url else None
            }

        # Follow pagination link to page 2
        next_page = response.xpath("//a[text()='Next']/@href").get()
        if next_page:
            yield response.follow(next_page, self.parse)
