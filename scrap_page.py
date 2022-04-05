import time
from loggers import log_warnings, log_events, log_extended_info
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException
from selenium.webdriver.common.keys import Keys


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def scrap_page(page):
    # Setting selenium web browser driver
    chrome_options = webdriver.ChromeOptions()
    # Browser console opens to hide Google ads in a footer of chrome window, witch interrupt clicks on page
    chrome_options.add_argument("--auto-open-devtools-for-tabs")
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    sub_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # Opening page
    driver.get(page['url'])
    # Close cookie setting request
    accept_cookie = driver.find_element(by=By.CLASS_NAME, value="uca-eu-all-accept")
    accept_cookie.click()

    # Retrieving info from page
    scraped_info_for_page = []

    # Finding offer and scraping info
    offers = driver.find_element(by=By.ID, value="spalte-1").find_elements(by=By.CLASS_NAME, value="arow")[1:]

    # Clicking "more details" button for every offer

    for offer in offers:
        # Passing titles
        if offer.get_attribute("class") == "arow row-title":
            continue
        # Click expand offer details in web browser
        # wait = WebDriverWait(offer, 10)
        try:
            expand_more_button = offer.find_element(by=By.CLASS_NAME, value="ad-roll")
            expand_more_button.click()
            # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ad-details')))
        except NoSuchElementException:
            log_warnings('no More_info button')
        except ElementClickInterceptedException:
            return False

    # Retrieving info from page.
    # Not in a previous cycle because selenium not waiting for roll down ad-details.
    time.sleep(1)
    scraped_info_from_page = []
    offers_len = len(offers)
    for offer_counter, offer in enumerate(offers):

        # Clearing buffer for this cycle
        offer_id = ''
        title = ''
        ad_details_text = ''
        details_list_dict = {}
        details_list_text = ''
        offer_contacts_in_details_dict = {}
        offer_contacts_in_details_text = ''
        contact_detail_date = ''
        offer_contacts_offer_date = ''
        offer_contacts_city = ''
        offer_author_name = ''
        author_name = ''
        place = ''
        phone_number = ''
        fax_number = ''
        email = ''

        # id    div id = {id}
        try:
            offer_id = offer.find_element(by=By.TAG_NAME, value="div").get_attribute("id")
            log_extended_info(['offer_id', offer_id])
        except NoSuchElementException:
            log_warnings('no id div ')

        # title div[1]/p.text
        try:
            title_html = offer.find_element(by=By.CLASS_NAME, value="anztextp") \
                .get_attribute("innerHTML").split('<div')[0].replace('&amp;', '&').split('<span class="ad-roll"')[0]
            log_extended_info(['title_html ', title_html])
            if '<a' in title_html:
                log_extended_info(['title_html.split(>)[1].split(</a>)[0]', title_html.split('>')[1].split('</a>')[0]])
                log_extended_info(['title_html.split(<br>)[1].replace()', title_html.split('<br>')[1].replace('"', '')])
                title = title_html.split('>')[1].split('</a>')[0].replace('</a', '') + title_html.split('<br>')[1].replace('"', '')
            else:
                title = title_html
            log_extended_info(['title', title])
        except NoSuchElementException:
            log_warnings('no anztextp')

        # Details text on other page
        try:
            details_link = offer.\
                find_element(by=By.XPATH, value='.//p[@class="anztextp"]/a').get_attribute("href")
            log_extended_info(['details_link', details_link])
            if details_link:
                sub_driver.get(details_link)
                log_extended_info(["link html: ",
                                  sub_driver.
                                  find_element(by=By.XPATH, value='.//fieldset[@class="ad_info_details"]/p').
                                  get_attribute("innerHTML")])
                page_detail_text = sub_driver.\
                    find_element(by=By.XPATH, value='.//fieldset[@class="ad_info_details"]/p').get_attribute("innerHTML")
                ad_details_text = remove_html_tags(page_detail_text)
                log_extended_info(['page_detail_text_notag', remove_html_tags(page_detail_text)])
        except NoSuchElementException:
            log_warnings('no details_link')

        # text div[class='ad-details']/div[0]/text
        try:
            ad_details_text = offer.find_element(by=By.CLASS_NAME, value='ad-details') \
                .find_element(by=By.TAG_NAME, value="div") \
                .text
            log_extended_info(['ad_details_text: ', ad_details_text])
        except NoSuchElementException:
            log_warnings('no ad-details')

        # details_list div[class='ad-details']/ul/[li]
        try:
            ad_details_list = offer \
                .find_element(by=By.CLASS_NAME, value='ad-details') \
                .find_element(by=By.TAG_NAME, value='ul') \
                .find_elements(by=By.TAG_NAME, value='li')
            for element in ad_details_list:
                # detail_name li/span
                details_lists_element_name = element.find_element(by=By.CLASS_NAME, value='em').text
                log_extended_info(['element: details_list_element_name', details_lists_element_name])
                # detail_value li.text
                details_lists_element_value = element.get_attribute("innerHTML") \
                    .split('</span>: ')[1].replace('&amp;', '&')
                log_extended_info(['element: details_list_element_value', details_lists_element_value])

                details_list_dict[details_lists_element_name] = details_lists_element_value

                if details_lists_element_name:
                    details_list_text = details_list_text +\
                                        details_lists_element_name + ': ' + details_lists_element_value + '; '
        except NoSuchElementException:
            log_warnings('no details list')
        log_extended_info(['details_list_dict', details_list_dict])
        log_extended_info(['details_list_text', details_list_text])

        # offer_contacts_in_details div[class='ad-details']/div[1:]/
        try:
            offer_contacts_in_details_list = offer \
                                                 .find_element(by=By.CLASS_NAME, value='ad-details') \
                                                 .find_elements(by=By.TAG_NAME, value='div')[1:]
            for detail in offer_contacts_in_details_list:
                log_extended_info(['contact detail', detail.get_attribute("innerHTML")])
                # details_contact
                contact_detail_name_html = detail.find_element(by=By.TAG_NAME, value='i').get_attribute("innerHTML")
                if '<b>' in contact_detail_name_html:
                    # offer.text "Объявление от: "
                    contact_detail_date_name = contact_detail_name_html.split('<b>')[0]
                    log_extended_info(['contact_detail_date_name', contact_detail_date_name])
                    # details_contact_value  b
                    contact_detail_date = detail.find_element(by=By.TAG_NAME, value='b').text
                    log_extended_info(['contact_detail_date', contact_detail_date])

                else:
                    # contact_detail_name
                    contact_detail_name = contact_detail_name_html
                    log_extended_info(['contact_detail_name', contact_detail_name])
                    # details_contact_value  b
                    contact_detail_value = detail.find_element(by=By.TAG_NAME, value='b').text
                    log_extended_info(['contact_detail_value', contact_detail_value])

                    offer_contacts_in_details_dict[contact_detail_name] = contact_detail_value
                    if contact_detail_name:
                        offer_contacts_in_details_text = offer_contacts_in_details_text + contact_detail_name + ': ' + contact_detail_value + '; '
        except NoSuchElementException:
            log_warnings('no offer_contacts_in_details')

        try:
            # offer_contacts p[class="anztextp"]/span[class="anztextp2"]
            offer_contacts = offer.find_element(by=By.CLASS_NAME, value='anztextp2') \
                .get_attribute("innerHTML").split('|')
            # date after i[0] before |
            if '<i>' in offer_contacts[0]:
                offer_contacts_offer_date = offer_contacts[0].split('</i>')[1]
                log_extended_info(['author_contacts_offer_date', offer_contacts_offer_date])
                offer_contacts_city = offer_contacts[1]
                log_extended_info(['offer_contacts_city', offer_contacts_city])
            # city after i[0] and |
            elif '<i>' not in offer_contacts[0]:
                offer_contacts_city = offer_contacts[0]
                log_extended_info(['offer_contacts_city', offer_contacts_city])
                if len(offer_contacts) > 1:
                    offer_author_name = offer_contacts[1].split('</i>')[1].replace('&nbsp;', '')
                    log_extended_info(['offer_author_name', offer_author_name])

        except NoSuchElementException:
            log_warnings('no author_contacts_dates')

        # author_contacts div[class="anztextp2"]
        try:
            # Finding base element of author contacts.
            # './/' in XPATH finds in this offer, not in the whole document
            author_contacts_container = offer.find_element(by=By.XPATH, value='.//div[@class="anztextp2"]') \
                .get_attribute("innerHTML").split('<br>')
            log_extended_info(['author_contacts_container', author_contacts_container])
            for contact_html in author_contacts_container:

                # name  before /
                if '<i>' in contact_html:
                    author_name = contact_html.split(' / ')[0].split('<b>')[1].split('</b>')[0].replace('&amp;', '&')
                    log_extended_info(['author_name ', author_name])
                # place after /
                if ' / ' in contact_html:
                    place = contact_html.split(' / ')[1].split('</b>')[0]
                    log_extended_info(['place', place])
                # tel 'Tel. ' in br.text /b
                if 'Tel' in contact_html:
                    phone_number = contact_html.split('<b>')[1].split('</b>')[0]
                    log_extended_info(['phone_number', phone_number])
                # fax 'Fax ' in br.text /b
                if 'Fax' in contact_html:
                    fax_number = contact_html.split('<b>')[1].split('</b>')[0]
                    log_extended_info(['fax_number', fax_number])
                # email b/span.text + '@' + b.text.replace(" ", "")
                if '<span>' in contact_html:
                    email = contact_html.split('<span>')[1].split('</span>')[0].replace(' ', '') + "@" + \
                        contact_html.split('</span>')[1].split('</b>')[0].replace(' ', '')
                    log_extended_info(['email', email])

        except NoSuchElementException:
            log_warnings('no author_contacts_dates')

        scraped_info_from_page_row = {
            'offer_id': offer_id,
            'section_id': page['section_id'],
            'section_name': page['section_name'],
            'category_name': page['category_name'],
            'sub_category_name': page['sub_category_name'],
            'lang': page['lang'],
            'title': title,
            'ad_details_text': ad_details_text,
            # 'details_list_json': json.dumps(details_list_dict),
            'details_list_text': details_list_text,
            'contact_detail_date': contact_detail_date,
            'offer_contacts_offer_date': offer_contacts_offer_date,
            'offer_contacts_city': offer_contacts_city,
            'offer_author_name': offer_author_name,
            'author_name': author_name,
            'place': place,
            'phone_number': phone_number,
            'fax_number': fax_number,
            'email': email
        }
        if offer_id:
            scraped_info_from_page.append(scraped_info_from_page_row)
        log_events('offer scraped:' + str(offer_counter) + '/' + str(offers_len))
    # time.sleep(500)
    return scraped_info_from_page
