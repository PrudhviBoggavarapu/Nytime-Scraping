# Readme

This project includes code for web scraping articles from The New York Times website and storing them in a database. The code is written in Python and utilises various libraries and tools such as BeautifulSoup, Selenium, polars.

## Prerequisites

Before running the code, ensure that you have the following prerequisites installed:

- Python 3.x
- BeautifulSoup: `pip install beautifulsoup4`
- Selenium: `pip install selenium`
- Polars: `pip install polars`
- Pandas: `pip install pandas`
- GeckoDriver: `pip install webdriver_manager` (for Firefox)

## Code Overview

The project consists of the following main components:

1. **Article Class**: Represents an article from The New York Times. It has attributes such as title, author, link, timestamp, alt text, and full text. It also provides methods for calculating the hash value of the article and converting it to a DataFrame.

2. **Web Scraping Functions**: Includes functions for finding elements, clicking elements, and starting the Selenium WebDriver with optional headless mode. These functions are used for navigating and interacting with the web pages.

4. **Database Creation**: Creates an empty database in CSV format if it doesn't already exist. The database will store the scraped articles.

5. **Scraping and Parsing**: Uses the generated URLs to retrieve the search results' HTML. The HTML is then parsed using BeautifulSoup to extract the relevant article information. The articles are parsed and converted into `Article` objects.

6. **Full Text Extraction**: Uses Selenium WebDriver to visit each article's link and extract the full text from the web page. The full text is then added to the respective `Article` object.

7. **Database Writing**: Writes the scraped articles to the database in CSV format. It checks for duplicate articles using the hash value and only adds new articles to the database.

## How to Use

To use this code, follow these steps:

1. Install the required libraries and tools mentioned in the "Prerequisites" section.

2. Copy the code provided into a Python file (e.g., `main.py`).

3. Modify the code as needed, such as adjusting the search query, date range, or database location.

4. Run the Python file using the command: `python main.py`

5. The code will scrape articles from The New York Times website, extract the full text, and store them in the specified database.

6. You can customise the code further to suit your specific needs, such as adding error handling, logging, or additional data processing.

## Notes

- The code is provided as a starting point and may require modifications or enhancements based on your specific requirements.
- Respect the website's terms of service and avoid excessive scraping that may cause harm or violate any policies.
- Always be mindful of web scraping ethics and legal considerations.
- Ensure you have the necessary permissions and rights to store and use the scraped data.

## Acknowledgements

This project utilises various open-source libraries and tools. We acknowledge their creators and contributors for their valuable contributions to the development community.
