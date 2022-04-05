from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# URl to web scrap from.
# in this example we web scrap graphics cards from Newegg.com
page_url = "https://anzeigen.ru-geld.de/%D1%83%D1%81%D0%BB%D1%83%D0%B3%D0%B8/%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%81%D1%82%D0%B5%D1%80%D1%81%D0%BA%D0%B8%D0%B5/"

# opens the connection and downloads html page from url
uClient = uReq(page_url)

# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(uClient.read(), "html.parser")
uClient.close()
# print(page_soup.prettify())
# finds each product from the store page
containers = page_soup.html.body.main.findAll("section")[1].findAll("div")[3].form.findAll("div", {"class": "arow"})
print(containers)
# name the output file to write to local disk
out_filename = "graphics_cards.csv"
# header of csv file to be written
headers = "offer_name \n"

# opens file, and writes headers
f = open(out_filename, "w")
f.write(headers)

# loops over each product and grabs attributes about
# each product
for container in containers:
    # Finds all link tags "a" from within the first div.
    # make_rating_sp = container.div.select("a")

    # Grabs the title from the image title attribute
    # # Then does proper casing using .title()
    # brand = make_rating_sp[0].img["title"].title()

    # Grabs the text within the second "(a)" tag from within
    # the list of queries.
    # offer_container = container.div.findAll("a", {"class": "item-title"})
    print(container.prettify())
    # print("\n product_info_container: ", product_info_container)
    # if product_info_container:
    #     offer_name = product_info_container[0].text
    # else:
    #     offer_name = ''
    # Grabs the product shipping information by searching
    # all lists with the class "price-ship".
    # Then cleans the text of white space with strip()
    # Cleans the strip of "Shipping $" if it exists to just get number
    # shipping = container.findAll("li", {"class": "price-ship"})[0].text.strip().replace("$", "").replace(" Shipping", "")

    # prints the dataset to console
    # print("brand: " + brand + "\n")
    # print("offer_name: " + offer_name + "\n")
    # print("shipping: " + shipping + "\n")

    # writes the dataset to file
    # f.write(offer_name.replace(",", "|") + ", " + offer_name + "\n")

f.close()  # Close the file


