import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrap_page import scrap_page

raise NotImplementedError

urls = [
"https://anzeigen.ru-geld.de/%D1%83%D1%81%D0%BB%D1%83%D0%B3%D0%B8/%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%81%D1%82%D0%B5%D1%80%D1%81%D0%BA%D0%B8%D0%B5/"
]

executor = ThreadPoolExecutor(10)


def scrape(url, *, loop):
    loop.run_in_executor(executor, scraper, url)


def scraper(url):
    # Setting selenium web browser driver
    chrome_options = webdriver.ChromeOptions()
    # Browser console opens to hide Google ads in a footer of chrome window, witch interrupt clicks on page
    chrome_options.add_argument("--auto-open-devtools-for-tabs");
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # Opening page
    driver.get(url)
    scrap_page(driver)


loop = asyncio.get_event_loop()
for url in urls:
    scrape(url, loop=loop)
loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(loop)))




