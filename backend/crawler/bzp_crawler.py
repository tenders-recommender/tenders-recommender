import datetime
import numpy as np

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
import json
import os
import time

from typing import List, Set

from tenders_recommender.dto import Interaction
from test.test_util import load_sorted_test_interactions

tmp_data = []
WHAT = "what"

old_offers_radio_xpath = '//input[@id="ctl00_ContentPlaceHolder1_rbBZP_Old"]'
offer_input_xpath = '//input[@name="ctl00$ContentPlaceHolder1$txtAnnouncementNumber"]'
search_xpath = '//input[@id="ctl00_ContentPlaceHolder1_btnSearch"]'
new_offers_radio_xpath = '//input[@id="ctl00_ContentPlaceHolder1_rbBZP_New"]'
result_row_css = 'tr.dxgvDataRow_Aqua'


def load_offers():
    interactions: List[Interaction] = load_sorted_test_interactions()
    offers_set: Set[str] = {interaction[WHAT] for interaction in interactions
                            if interaction[WHAT].__contains__("bzp")}
    return offers_set


def parse_offers_set(offers_set: Set):
    offers_ids: List[str] = []
    for offer in offers_set:
        if offer.startswith("bzp"):
            split = offer.rsplit('-')
            year = split[1].strip()
            id = split[-1].strip()
            offers_ids.append(id + "-N-" + year)
        else:
            split_ = offer.rsplit('_')
            year = split_[0].strip()
            id = split_[2].strip()
            offers_ids.append(id + "-" + year)
    return offers_ids


def isElementSelected(xpath):
    try:
        return WebDriverWait(driver, 3).until(EC.element_located_to_be_selected((By.XPATH, xpath)))
    except:
        return False


def isElementFound(xpath):
    try:
        return WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except:
        return False


def selectElement(xpath):
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
    except:
        print("cannot select offers button")


def clickSearch(xpath):
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
    except:
        print("Search click failed")


def clear_text(xpath):
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).clear()
    except:
        print("Clear text failed")


def sendText(xpath, text):
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(text)
    except:
        print("Send text failed")


def save_data(html, id):
    try:
        row = Selector(text=html).css(result_row_css)
        tmp_data.append({row.css("td.dxgv::text")[1].extract(): row.css("td.dxgv::text")[6].extract()})
    except:
        print("fail to get offer " + id)


def find_data(offers_radio_button_xpath, id):
    selectElement(offers_radio_button_xpath)
    clear_text(offer_input_xpath)
    sendText(offer_input_xpath, id)
    clickSearch(search_xpath)
    searched_element_xpath = '//td[contains(text(),"' + id + '")]'
    found = isElementFound(searched_element_xpath)
    if found:
        html = driver.page_source
        save_data(html, id)
    return found


def scrape_offers(offers_ids):
    global tmp_data
    print(len(offers_ids))
    num_of_ids = 1
    for id in offers_ids:

        if num_of_ids % 500 == 0:
            file_path = "description" + str(i) + ".json"
            with open(file_path, "a") as json_file:
                json.dump(tmp_data, json_file)
            while not os.path.exists(file_path):
                time.sleep(1)

        if not find_data(old_offers_radio_xpath, id):
            find_data(new_offers_radio_xpath, id)

        num_of_ids += 1


if __name__ == '__main__':
    offers_ids = parse_offers_set(load_offers())
    chrome_folder_path = os.path.join(os.getcwd(), 'chromedriver')
    chrome_path = os.path.join(chrome_folder_path, 'chromedriver')
    driver = webdriver.Chrome(chrome_path)

    driver.get('https://searchbzp.uzp.gov.pl/Search.aspx')

    start = datetime.datetime.now()
    scrape_offers(offers_ids)
    end = datetime.datetime.now()
    print(end - start)

    with open("description_final.json", "a") as json_file:
        json.dump(tmp_data, json_file)
    driver.close()
