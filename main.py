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
die_event = threading.Event()
raw_html_queue = queue.Queue()
writing_class_queue = queue.Queue()



def do_the_scraping(die_event: threading.Event, ):
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
            raw_html_queue.put(page_source)
    except:
        driver.quit()
        exit_event.set()



def WritingDataBase(
    die_event: threading.Event, writing_class_queue: queue.Queue, database_location: str
):
    testing_dataframe = pl.DataFrame(schema=Article.parse_schema())

    while not die_event.is_set():
        try:
            raw_element: Article = writing_class_queue.get_nowait()
            data_frame_element = raw_element.to_dataframe()
            testing_dataframe.extend(data_frame_element)
            print(testing_dataframe[-1][0])
        except queue.Empty:
            pass
    print('writiing data')
    testing_dataframe.write_csv(database_location, separator="|")
    print("all Done")


try:
    Sending_Raw_Html_Thread = threading.Thread(target=do_the_scraping)



    Converting_Html_To_Classs = threading.Thread(
        target=handle_raw_html,
        args=(die_event, raw_html_queue, database_location, writing_class_queue),
    )

    Writing_Data_To_File = threading.Thread(
        target=WritingDataBase,
        args=(
            die_event,
            writing_class_queue,
            database_location,
        ),
    )
    Sending_Raw_Html_Thread.start()
    Converting_Html_To_Classs.start()
    Writing_Data_To_File.start()

    # Wait for KeyboardInterrupt
    while True:
        sleep(.1)

except KeyboardInterrupt:
    # Set the die_event to stop the threads
    die_event.set()

    # Wait for the threads to finish
    Sending_Raw_Html_Thread.join()
    Converting_Html_To_Classs.join()
    Writing_Data_To_File.join()

    print("Threads stopped.")
