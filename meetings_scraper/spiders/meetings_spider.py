import scrapy
from datetime import datetime
import re

class MeetingsSpider(scrapy.Spider):
    name = "meetings"
    start_urls = ["https://symonsrec.com/info/minutes/"]

    def parse(self, response):
        try:
            title_raw = response.xpath('//*[@id="post-750"]/div/div[1]/div/div/div/div/div/div/div[1]/h1/text()').get()
            title = title_raw.split("–")[1]
            for row in response.xpath("//table/tbody/tr"):
                doc_links = row.xpath("./td[2]/a | ./td[3]/a | ./td[4]/a") 
                if doc_links:
                    for doc_link in doc_links:
                        try:
                            doc_name = doc_link.xpath("text()").get()

                            # Check if the document name exists
                            if doc_name:
                                date = self.extract_date(doc_name)
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

    def extract_date(self, doc_name):
        try:
            raw_date = re.search(r'(\w+ \d{1,2}, \d{4})', doc_name)
            if raw_date:
                extracted_date = raw_date.group(1)
                formatted_date = datetime.strptime(extracted_date, "%B %d, %Y").strftime("%Y-%m-%d")
                return formatted_date
            else:
                self.logger.warning(f"No date found in document name: {doc_name}")
                return None
        except ValueError as e:
            self.logger.error(f"Date format error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error in extract_date: {e}")
            return None
