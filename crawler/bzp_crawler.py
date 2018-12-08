import datetime
import numpy as np

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
import os
import platform

from typing import List, Set, Dict

from tenders_recommender.dao import DescriptionsDao
from tenders_recommender.database import init_database, Session
from tenders_recommender.model import Interaction, Descriptions
from benchmarks.test_util import load_sorted_test_interactions

WHAT = "what"

old_offers_radio_xpath = '//input[@id="ctl00_ContentPlaceHolder1_rbBZP_Old"]'
offer_input_xpath = '//input[@name="ctl00$ContentPlaceHolder1$txtAnnouncementNumber"]'
search_xpath = '//input[@id="ctl00_ContentPlaceHolder1_btnSearch"]'
new_offers_radio_xpath = '//input[@id="ctl00_ContentPlaceHolder1_rbBZP_New"]'
result_row_css = 'tr.dxgvDataRow_Aqua'
bzp_site = 'https://searchbzp.uzp.gov.pl/Search.aspx'


def load_offers():
    interactions: List[Interaction] = load_sorted_test_interactions()
    offers_set: Set[str] = {interaction[WHAT] for interaction in interactions
                            if interaction[WHAT].__contains__("bzp")}
    return offers_set


def parse_offers_set(offers_set: Set) -> List[str]:
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


def isElementSelected(xpath: str) -> bool:
    try:
        return WebDriverWait(driver, 3).until(EC.element_located_to_be_selected((By.XPATH, xpath)))
    except:
        try:
            return WebDriverWait(driver, 3).until(EC.element_located_to_be_selected((By.XPATH, xpath)))
        except:
            return False


def isElementFound(xpath: str) -> bool:
    try:
        return WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except:
        try:
            return WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except:
            return False


def selectElement(xpath: str) -> None:
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
    except:
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
        except:
            print("cannot select offers button")


def clickSearch(xpath: str) -> None:
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
    except:
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
        except:
            print("Search click failed")


def clear_text(xpath: str) -> None:
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).clear()
    except:
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).clear()
        except:
            print("Clear text failed")


def sendText(xpath: str, text: str):
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(text)
    except:
        try:
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(text)
        except:
            print("Send text failed")


def get_record(html: str, id: str) -> Dict:
    try:
        row = Selector(text=html).css(result_row_css)
        return {row.css("td.dxgv::text")[1].extract(): row.css("td.dxgv::text")[6].extract()}
    except:
        print("fail to get offer " + id)


def find_data(offers_radio_button_xpath: str, id: str) -> Dict:
    selectElement(offers_radio_button_xpath)
    clear_text(offer_input_xpath)
    sendText(offer_input_xpath, id)
    clickSearch(search_xpath)
    searched_element_xpath = '//td[contains(text(),"' + id + '")]'
    found = isElementFound(searched_element_xpath)
    record = None
    if found:
        html = driver.page_source
        record = get_record(html, id)
    return record


def scrape_offers(offers_ids: List[str]) -> List[str]:
    tmp_data: List[str] = []
    print(len(offers_ids))
    for id in offers_ids:
        record = find_data(old_offers_radio_xpath, id)
        if record is None:
            record = find_data(new_offers_radio_xpath, id)
        if record is not None:
            tmp_data.append(record)
    return tmp_data


def parse(tmp_data) -> Dict[str, str]:
    descriptions_dict: Dict[str, str] = dict()

    for complex_description in tmp_data:
        offer, description = complex_description.popitem()
        better_offer = offer.replace('-N-', '-')
        descriptions_dict[better_offer] = description
    return descriptions_dict


def start_crawler(offers_ids: List[str]):
    init_database()
    sub_ofers_ids = [offers_ids[i:i + 1000] for i in range(0, len(offers_ids), 1000)]
    for sub_ids in sub_ofers_ids:
        tmp_data = scrape_offers(sub_ids)
        descriptions_dict = parse(tmp_data)
        descriptions_dao = DescriptionsDao()
        descriptions_dao.insert_description(Descriptions(descriptions_dict))
    Session.close()


if __name__ == '__main__':
    offers_ids = parse_offers_set(load_offers())
    chrome_folder_path = os.path.join(os.getcwd(), 'chromedriver')
    chrome_file_name = 'chromedriver' if platform.system() == 'Linux' else 'chromedriver.exe'
    chrome_path = os.path.join(chrome_folder_path, chrome_file_name)

    driver = webdriver.Chrome(chrome_path)

    driver.get(bzp_site)

    start = datetime.datetime.now()
    start_crawler(offers_ids)
    end = datetime.datetime.now()
    print(end - start)

    driver.close()
