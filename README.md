# Scrapy Web Scraping Challenge: Government Meeting Documents

This project is a **Scrapy-based web scraper** designed to extract metadata from meeting documents listed on the [Symons Recreation](https://symonsrec.com/info/minutes/) website. The spider retrieves essential details such as meeting date, title, category, and document URLs.

## Features

- **Meeting Documents Extraction**: Scrapes and organizes metadata from meeting records.
- **Pagination Handling**: Extracts meeting documents from **the first two pages**.
- **Error Logging**: Logs warnings and errors for debugging.
- **CSV Export**: Stores extracted data in a structured `.csv` format.

## Requirements

- **Python 3.x**
- **Scrapy framework** (`pip install scrapy`)
- **Ability to run a Scrapy project** (`scrapy crawl meetings`)

## Installation

1. Clone the repository and navigate to the project folder:
   ```bash
   git clone <repository-url>
   cd meetings_scraper

## Running the Spider

To execute the scraper and output a CSV file:
 ```bash
 scrapy crawl meetings -o meetings.csv 
 ```
This will extract meeting documents and save them in meetings.csv.

## Technologies Used
**Python**: Primary programming language for extraction.

**Scrapy**: Web scraping framework.

**Regex**: Used for extracting dates from document titles.

**CSV Export**: Data saved in structured format.
