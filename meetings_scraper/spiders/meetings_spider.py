import scrapy
from datetime import datetime
import re
from dateutil import parser

class MeetingsSpider(scrapy.Spider):
    name = "meetings"
    start_urls = ["https://symonsrec.com/info/minutes/"]

    def parse(self, response):
        try:
            title_raw = response.xpath('//div[@class="column2"]//h1/text()').get()
            title = title_raw.split("–")[1]
            for row in response.xpath("//table/tbody/tr"):
                doc_links = row.xpath("./td[2]/a | ./td[3]/a | ./td[4]/a") 
                if doc_links:
                    for doc_link in doc_links:
                        try:
                            doc_name = doc_link.xpath("text()").get()

                            # Check if the document name exists
                            if doc_name:
                                date = parser.parse(' '.join(doc_name.rsplit(' ')[:-1])).strftime('%Y-%m-%d')
                                category = doc_name.split()[-1].strip() if doc_name.split() else "other"
                                url = doc_link.xpath("@href").get()
                                meeting_title = doc_name + " " + title if title else doc_name
                                yield {
                                    "Date": date,
                                    "Meeting_title": meeting_title,
                                    "Category": category,
                                    "Url": url
                                }
                            else:
                                self.logger.warning("No document link found in the row.")
                        except Exception as e:
                            self.logger.error(f"Error processing document link: {e}")
                else:
                    self.logger.warning("No document links found in the row.")

        except Exception as e:
            self.logger.error(f"Error parsing response: {e}")