import scrapy
from datetime import datetime
import re

class MeetingsSpider(scrapy.Spider):
    name = "meetings"
    start_urls = ["https://symonsrec.com/info/minutes/"]

    def parse(self, response):
        for row in response.xpath("//table/tbody/tr"):

            category_link = row.xpath("./td[3]/a")  
            category = category_link.xpath("text()").get()
            #condition to check if the document is present or not
            if category:
                date_match = re.search(r'(\w+ \d{1,2}, \d{4})', category)
                formatted_date = None
                if date_match:
                    try:
                        extracted_date = date_match.group(1)
                        formatted_date = datetime.strptime(extracted_date, "%B %d, %Y").strftime("%Y-%m-%d")
                    except ValueError:
                        formatted_date = None
                url = category_link.xpath("@href").get()
                
            else:
                category = "other"
                url = None
            raw_date = row.xpath("./td[1]/text()").get()
            meeting_title = row.xpath("./td[2]/text()").get()
            

             # Convert date to yyyy-mm-dd format
            formatted_date = None
            if raw_date:
                try:
                    formatted_date = datetime.strptime(raw_date.strip(), "%m/%d/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    formatted_date = raw_date.strip()  # Keep original if parsing fails

            yield {
                "date":formatted_date,
                "meeting_title": meeting_title.strip() if meeting_title else None,
                "category": category.strip() if category else None,
                "URL": response.urljoin(url) if url else None
            }

        # Follow pagination link to page 2
        next_page = response.xpath("//a[text()='Next']/@href").get()
        if next_page:
            yield response.follow(next_page, self.parse)
