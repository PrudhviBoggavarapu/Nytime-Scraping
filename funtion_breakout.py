import polars as pl
from time import sleep
from bs4 import BeautifulSoup

import glob
import queue
import threading
import os
import polars as pl
import pandas as pd
from time import sleep
from pprint import pprint
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager




class Article:
    def __init__(self, title, author, link, timestamp, alt_text):
        self.title = title
        self.author = author
        self.link = link
        self.timestamp = timestamp
        self.alt_text = alt_text

    def to_dataframe(self):
        data = {
            "title": [self.title],
            "author": [self.author],
            "link": [self.link],
            "timestamp": [self.timestamp],
            "alt_text": [self.alt_text]
        }
        schema = self.parse_schema()
        return pl.DataFrame(data, schema=schema)

    @staticmethod
    def parse_schema():
        schema = {
            "title": str,
            "author": str,
            "link": str,
            "timestamp": pl.Int64,
            "alt_text": str
        }

        return
    @staticmethod
    def parse_article(li_object):
        article_element = li_object
        if not article_element:
            return None

        title_element = article_element.find("h4")
        author_element = article_element.find("p")
        link_element = article_element.find("a")
        date_element = article_element.find("span")
        image_element = article_element.find("img")

        title = title_element.text.strip() if title_element else None
        author = author_element.text.strip() if author_element else None
        link = f'https://www.nytimes.com{link_element["href"]}' if link_element else None
        date = date_element["aria-label"] if date_element else None
        alt_text = (
            image_element["alt"] if image_element and "alt" in image_element.attrs else None
        )

        timestamp = None
        if date:
            try:
                timestamp = int(datetime.strptime(date, "%B %d, %Y").timestamp())
            except ValueError:
                timestamp = 0

        return Article(title, author, link, timestamp, alt_text)







    def __str__(self):
        return f"Title: {self.title}\nAuthor: {self.author}\nLink: {self.link}\nTimestamp: {self.timestamp}\nAlt Text: {self.alt_text}"

def find_element(driver, selector, method=By.CSS_SELECTOR):
    methods = {
        By.CSS_SELECTOR: By.CSS_SELECTOR,
        By.XPATH: By.XPATH,
        By.ID: By.ID,
        By.NAME: By.NAME,
        By.CLASS_NAME: By.CLASS_NAME,
        By.TAG_NAME: By.TAG_NAME,
        By.LINK_TEXT: By.LINK_TEXT,
        By.PARTIAL_LINK_TEXT: By.PARTIAL_LINK_TEXT,
    }
    if method not in methods:
        raise ValueError("Invalid method provided. Use a valid 'By' constant.")

    return driver.find_element(methods[method], selector)

def click_element(driver, selector, method=By.CSS_SELECTOR):
    element = find_element(driver, selector, method)
    element.click()

def start_driver():
    options = Options()
    # options.set_preference("javascript.enabled", False)
    folder_path = "extentions/"
    xpi_files = glob.glob(folder_path + "*.xpi")
    driver = webdriver.Firefox(options=options)
    for xpi_path in xpi_files:
        driver.install_addon(xpi_path, temporary=True)
    window_handles = driver.window_handles
    for handle in window_handles[1:]:
        driver.switch_to.window(handle)
        driver.close()
    driver.switch_to.window(window_handles[0])
    driver.implicitly_wait(1)

    return driver

def generateUrls(query, start_date="1920-01-01", end_date=datetime.now().strftime("%Y-%m-%d"), freq="180D"):
    dateRange = pd.date_range(start=start_date, end=end_date, freq=freq)
    date_ranges = [
        (date.strftime("%Y%m%d"), (date + pd.Timedelta(days=180)).strftime("%Y%m%d"))
        for date in dateRange
    ]
    date_ranges[-1] = (date_ranges[-1][0], datetime.now().strftime("%Y%m%d"))

    return [
        f"https://www.nytimes.com/search?dropmab=false&endDate={y}&query={query}&sort=best%2Cnewest&startDate={x}&types=article"
        for x, y in date_ranges
    ]

def create_database():
    csv_file = "database.csv"
    if not os.path.exists(csv_file):
        data = {
            "title": "",
            "author": "",
            "link": "",
            "timestamp": None,
            "alt_text": ""
        }
        schema = {
                    "title": str,
                    "author": str,
                    "link": str,
                    "timestamp": pl.Int64,
                    "alt_text": str
                }
        empty_artical = pl.DataFrame(data)
        empty_artical.write_csv(csv_file)
        
        
        



def handle_raw_html(exit_event,page_queue,database_location):
    while True:
        if exit_event.is_set():
            break
        try:
            item = page_queue.get_nowait()
            soup = BeautifulSoup(item, "html.parser")

            open("file.html", "w+").write(item)

            ol_element = soup.find("ol", {"data-testid": "search-results"})
            li_elements = ol_element.find_all("li", recursive=False)

            schema = Article.parse_schema()
            read_csv_data = pl.read_csv(database_location, dtypes=schema)


            for li in li_elements:
                article = Article.parse_article(li)
                fixed_data = article.to_dataframe()
                print(read_csv_data.dtypes)
                print(fixed_data.dtypes)
                read_csv_data.extend(fixed_data)                
                
                print(fixed_data)

            read_csv_data.write_csv(database_location)

        except queue.Empty:
            pass

