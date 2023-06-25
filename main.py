import os
import glob
import queue
import threading
import polars as pl
import pandas as pd
from time import sleep
from pprint import pprint
from funtion_breakout import *
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

database_location = "database.csv"





driver = start_driver()


search_params = "evangelical"

# driver.get(f'https://www.nytimes.com/search?dropmab=false&endDate=20230501&query={search_params}&sort=best%2Cnewest&startDate=20220601&types=article')

driver.implicitly_wait(1)

exit_event = threading.Event()

page_queue = queue.Queue()


def do_the_scraping():
    try:
        for n in generateUrls(search_params)[-5:-1]:
            driver.get(n)
            while True:
                try:
                    find_element(
                        driver, 'button[data-testid="search-show-more-button"]'
                    ).click()
                    sleep(0.5)
                except NoSuchElementException as e:
                    break
            page_source = driver.page_source
            page_queue.put(page_source)
    except:
        driver.quit()
        exit_event.set()


def create_database():
    csv_file = "database.csv"
    if not os.path.exists(csv_file):
        Article = Article("","","","","").parse_article()
        Article.write_csv(csv_file)


def handle_raw_html():
    while True:
        if exit_event.is_set():
            break
        try:
            item = page_queue.get_nowait()
            soup = BeautifulSoup(item, "html.parser")

            open("file.html", "w+").write(item)

            ol_element = soup.find("ol", {"data-testid": "search-results"})
            li_elements = ol_element.find_all("li", recursive=False)
            read_csv_data = pl.read_csv(database_location)

            for li in li_elements:
                article = Article.parse_article(li)
                print(article.title)
                print(article.to_dataframe())
           
            data = pl.from_dict({



            })
            read_csv_data.write_csv(database_location)

        except queue.Empty:
            pass


create_database()


producer = threading.Thread(target=do_the_scraping)
consumer = threading.Thread(target=handle_raw_html)

producer.start()
consumer.start()
