import os
import json
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class QuoteScraper:
    def __init__(self):
        self.quotes_final = []
        self.about_author = {}
        self.data_final = {}
        self.find_author = 'J.K. Rowling'

    def get_data(self):
        url = 'https://quotes.toscrape.com/'

        browser = Chrome()
        browser.get(url)

        while True:
            quotes = browser.find_elements(By.CLASS_NAME, 'quote')
            self.quotes_organize(quotes)

            try:
                next_button = browser.find_element(By.CLASS_NAME, 'next')
                next_link = next_button.find_element(By.TAG_NAME, 'a')
                next_link.click()
            except NoSuchElementException:
                break

        self.data_final['quotes'] = self.quotes_final

        self.get_author_data(browser)

        filename = f'./output/data.json'
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w') as file:
            json.dump(self.data_final, file, indent=4)

        browser.quit()

    def quotes_organize(self, quotes):
        for quote in quotes:
            author = quote.find_element(By.CLASS_NAME, 'author')
            if author.text == self.find_author:
                self.about_author = quote.find_element(By.TAG_NAME, 'a')
                quote_aux = {}
                quote_aux['text'] = quote.find_element(By.CLASS_NAME, 'text').text
                tags = quote.find_elements(By.CLASS_NAME, 'tag')
                tags_final = []
                for tag in tags:
                    tags_final.append(tag.text)
                quote_aux['tags'] = tags_final
                self.quotes_final.append(quote_aux)
    
    def get_author_data(self, browser):
        self.about_author.click()
        details = browser.find_element(By.CLASS_NAME, 'author-details')

        self.data_final['name'] = details.find_element(By.CLASS_NAME, 'author-title').text
        born_date = details.find_element(By.CLASS_NAME, 'author-born-date').text
        born_location = details.find_element(By.CLASS_NAME, 'author-born-location').text
        self.data_final['born'] = born_date + born_location
        self.data_final['description'] = details.find_element(By.CLASS_NAME, 'author-description').text[:140] + '...'
