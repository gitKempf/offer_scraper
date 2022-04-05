import time
from scrap_categories import scrap_pages_from_categories
from scrap_page import scrap_page
from save_to_file import save_to_file
from sections import sections


# Scraping Categories
pages = []
sections_length = len(sections)
for categories_scraped_counter, section in enumerate(sections):
    for attempt in range(5):
        print(section)
        scraped_pages = scrap_pages_from_categories(section)
        pages.extend(scraped_pages)
        if scraped_pages:
            print('Scraped: ', str(categories_scraped_counter), '/', str(sections_length))
            scraped_pages = []
            break
        else:
            print('section not scraped: ', section['name'])
        time.sleep(1)


print('Categories scraped. Begin scrapping pages')
time.sleep(5)
# Lopping throw given pages, scrapping it and saving to file
pages_length = len(pages)
for pages_scraped_counter, page in enumerate(pages):
    result = False
    for attempt in range(5):
        scrap_result = scrap_page(page)
        if scrap_result:
            print('Pages_scraped: ', str(pages_scraped_counter), '/', str(pages_length))
            save_to_file(scrap_result)
            break
    else:
        print('url not scraped: ', page['url'])

    # Pausing to avoid DDoS-ing server
    time.sleep(1)




