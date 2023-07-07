import glob
import queue
import threading
import os
import polars as pl
import pandas as pd
from typing import Type
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

database_location = "database.csv"
die_event = threading.Event()
raw_html_queue = queue.Queue()
writing_class_queue = queue.Queue()
get_full_text_queue = queue.Queue()


def testing_stuff(page_queue, exit_event):
    data = open("file.html", "r").read()
    page_queue.put(data)
    sleep(1000)
    exit_event.set()
    print('All Done testing')

try:
    Sending_Raw_Html_Thread = threading.Thread(
        target=testing_stuff,
        args=(
            raw_html_queue,
            die_event,
        ),
    )

    Converting_Html_To_Classs = threading.Thread(
        target=handle_raw_html,
        args=(die_event, raw_html_queue, database_location, get_full_text_queue),
    )


    Converting_Links_To_Full_Text_Data = threading.Thread(
        target=Links_To_Full_Text_Data,
        args=(die_event, get_full_text_queue, writing_class_queue),
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
    Converting_Links_To_Full_Text_Data.start()
    Converting_Html_To_Classs.start()
    Writing_Data_To_File.start()

    # Wait for KeyboardInterrupt
    while True:
        sleep(.1)

        
        if not (Sending_Raw_Html_Thread.is_alive() and Converting_Html_To_Classs.is_alive() and Converting_Links_To_Full_Text_Data.is_alive() and Writing_Data_To_File.is_alive()):
            print('DIE')
            die_event.set()
            break









except KeyboardInterrupt:
    # Set the die_event to stop the threads
    die_event.set()
    print("Threads stopped.")





exit()
