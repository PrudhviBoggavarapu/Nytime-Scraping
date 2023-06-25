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
from funtion_breakout import * 


def testing_stuff(page_queue, exit_event):
    print(11)
    data = open('file.html', 'r').read()
    page_queue.put(data)
    sleep(10)
    exit_event.set()

database_location = "database.csv"




exit_event = threading.Event()
page_queue = queue.Queue()




create_database()
producer = threading.Thread(target=testing_stuff, args=(page_queue,exit_event,))
consumer = threading.Thread(target=handle_raw_html, args=(exit_event,page_queue,database_location,))

producer.start()
consumer.start()
