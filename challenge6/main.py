import json
from quote_scraper import QuoteScraper

def main():
    scraper = QuoteScraper()
    scraper.get_data()

    print(json.dumps(scraper.data_final, indent=4))

if __name__ == "__main__":
    main()
