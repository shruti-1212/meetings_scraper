import scrapy
from datetime import datetime
import re

class MeetingsSpider(scrapy.Spider):
    name = "meetings"
    start_urls = ["https://symonsrec.com/info/minutes/"]

    def parse(self, response):
        for row in response.xpath("//table/tbody/tr"):

            doc_links = row.xpath("./td[2]/a | ./td[3]/a")
            if doc_links:
                for doc_link in doc_links:
                    doc_name = doc_link.xpath("text()").get()

                    #condition to check if the meeting document is present or not
                    if doc_name:
                        date = self.extract_date(doc_name)
                        category = doc_name.split()[-1].strip()
                        url = doc_link.xpath("@href").get()

                        yield {
                            "Date":date,
                            "Meeting_title": None,
                            "Category": category,
                            "Url": url}
                    else:
                        self.logger.warning("No document link found in the row.")


    def extract_date(self, doc_name):
        raw_date = re.search(r'(\w+ \d{1,2}, \d{4})', doc_name)
        formatted_date = None
        if raw_date:
            extracted_date = raw_date.group(1)
            formatted_date = datetime.strptime(extracted_date, "%B %d, %Y").strftime("%Y-%m-%d")
            return formatted_date

