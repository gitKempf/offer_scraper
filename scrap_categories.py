import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException
from selenium.webdriver.common.keys import Keys


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def scrap_pages_from_categories(section):
    # Setting selenium web browser driver
    chrome_options = webdriver.ChromeOptions()
    # Browser console opens to hide Google ads in a footer of chrome window, witch interrupt clicks on page
    chrome_options.add_argument("--auto-open-devtools-for-tabs")
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(section['url'])
    # Close cookie setting request
    try:
        accept_cookie = driver.find_element(by=By.CLASS_NAME, value="uca-eu-all-accept")
        accept_cookie.click()
    except NoSuchElementException:
        print('no accept cookie button')

    # Finding sub_categories on section page
    categories = []
    try:
        categories = driver.find_elements(by=By.XPATH, value='//ul[@class = "noel w-50-pr fll m2-clear m3-clear"]/li')
        print('categories', categories)
    except NoSuchElementException:
        print('no categories')
        return []
    category_name = ''
    scraped_categories = []
    for category in categories:
        print(category.get_attribute("innerHTML"))

        # Clearing buffer for this cycle
        sub_category_name = ''
        sub_category_url = ''

        # Finding category
        try:
            if category.get_attribute("class") == 'noel':
                category_name = category.find_element(by=By.TAG_NAME, value="h3").text
                # print('category_name', category_name)
        except NoSuchElementException:
            print('no tag')

        # Finding sub_category
        try:
            if category.get_attribute("class") != 'noel':
                sub_category = category.find_element(by=By.TAG_NAME, value="a")
                # name
                sub_category_name = sub_category.text
                print('sub_category_name', sub_category_name)
                # url
                sub_category_url = sub_category.get_attribute("href")
                print('sub_category_url', sub_category_url)

        except NoSuchElementException:
            print('no <a> in sub_category')

        scraped_category = {
            'section_id': section['section_id'],
            'section_name': section['name'],
            'lang': section['lang'],
            'category_name': category_name,
            'sub_category_name': sub_category_name,
            'url': sub_category_url
        }
        if sub_category_url:
            scraped_categories.append(scraped_category)
    # print(scraped_categories)
    # time.sleep(500)
    return scraped_categories
