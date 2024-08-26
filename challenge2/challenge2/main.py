__author__ = "Sthefany Martins"
__version__ = "0.1.0"

import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def main(argument):
    process = CrawlerProcess(get_project_settings())
    process.crawl('servimed-spider', argument=argument)
    process.start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <order_id>")
        sys.exit(1)

    argument = sys.argv[1]
    main(argument)
