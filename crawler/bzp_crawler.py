import datetime
from collections import ChainMap
from itertools import accumulate, chain, repeat, tee


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
import os
import platform

from typing import List, Set, Dict

from tenders_recommender.dao import DescriptionsDao, UsersInteractionsDao
from tenders_recommender.database import init_database, Session
from tenders_recommender.model import Descriptions

WHAT = "what"

old_offers_radio_xpath = '//input[@id="ctl00_ContentPlaceHolder1_rbBZP_Old"]'
offer_input_xpath = '//input[@name="ctl00$ContentPlaceHolder1$txtAnnouncementNumber"]'
search_xpath = '//input[@id="ctl00_ContentPlaceHolder1_btnSearch"]'
new_offers_radio_xpath = '//input[@id="ctl00_ContentPlaceHolder1_rbBZP_New"]'
result_row_css = 'tr.dxgvDataRow_Aqua'
bzp_site = 'https://searchbzp.uzp.gov.pl/Search.aspx'


def load_offers() -> List[str]:
    interactions = UsersInteractionsDao.query_all_users_interactions()
    all_interactions = list(chain.from_iterable(map(lambda inter: inter.users_interactions, interactions)))
    offers_set: Set[str] = {interaction[WHAT] for interaction in all_interactions
                            if interaction[WHAT].__contains__("bzp")}
    offers = parse_offers_set(offers_set)
    print("Number of all offers: " + str(len(offers_set)))

    descriptions_dao = DescriptionsDao()
    results = descriptions_dao.query_all_descriptions()
    descriptions_list: List = []
    for result in results:
        descriptions_list.append(result.data)
    descriptions = dict(ChainMap(*descriptions_list))

    unique_offers_list: List[str] = []
    for offer_id in offers:
        parsed_id = offer_id.replace('-N-', '-')
        if parsed_id not in descriptions:
            unique_offers_list.append(offer_id)

    print("Number of offers without description: " + str(len(unique_offers_list)))
    return unique_offers_list


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


def isElementSelected(xpath: str, driver) -> bool:
    try:
        return WebDriverWait(driver, 1).until(EC.element_located_to_be_selected((By.XPATH, xpath)))
    except:
        try:
            return WebDriverWait(driver, 1).until(EC.element_located_to_be_selected((By.XPATH, xpath)))
        except:
            return False


def isElementFound(xpath: str, driver) -> bool:
    try:
        return WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except:
        try:
            return WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except:
            return False


def selectElement(xpath: str, driver) -> None:
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
    except:
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
        except:
            print("cannot select offers button")


def clickSearch(xpath: str, driver) -> None:
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
    except:
        print("Search click failed, trying again")
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath))).click()
        except:
            print("Search click failed second time")


def clear_text(xpath: str, driver) -> None:
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath))).clear()
    except:
        print("Clear text failed, trying again..")
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath))).clear()
        except:
            print("Clear text failed second time")


def sendText(xpath: str, text: str, driver):
    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(text)
    except:
        print("Send text failed, trying again")
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(text)
        except:
            print("Send text failed second time")


def get_record(html: str, id: str) -> Dict:
    try:
        row = Selector(text=html).css(result_row_css)
        return {row.css("td.dxgv::text")[1].extract(): row.css("td.dxgv::text")[6].extract()}
    except:
        print("fail to get offer " + id)


def find_data(offers_radio_button_xpath: str, id: str, driver) -> Dict:
    selectElement(offers_radio_button_xpath, driver)
    clear_text(offer_input_xpath, driver)
    sendText(offer_input_xpath, id, driver)
    clickSearch(search_xpath, driver)
    searched_element_xpath = '//td[contains(text(),"' + id + '")]'
    found = isElementFound(searched_element_xpath, driver)
    record = None
    if found:
        html = driver.page_source
        record = get_record(html, id)
    return record


def scrape_offers(offers_ids: List[str], driver) -> List[str]:
    tmp_data: List[str] = []
    print(len(offers_ids))
    for id in offers_ids:
        record = find_data(old_offers_radio_xpath, id, driver)
        if record is None:
            record = find_data(new_offers_radio_xpath, id, driver)
        if record is not None:
            tmp_data.append(record)
        driver.refresh()
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
    chrome_folder_path = os.path.join(os.getcwd(), 'chromedriver')
    chrome_file_name = 'chromedriver' if platform.system() == 'Linux' else 'chromedriver.exe'
    chrome_path = os.path.join(chrome_folder_path, chrome_file_name)
    driver = webdriver.Chrome(chrome_path)
    driver.get(bzp_site)

    sub_ofers_ids = [offers_ids[i:i + 100] for i in range(0, len(offers_ids), 100)]
    for sub_ids in sub_ofers_ids:
        start = datetime.datetime.now()
        tmp_data = scrape_offers(sub_ids, driver)
        descriptions_dict = parse(tmp_data)
        print("found " + str(len(descriptions_dict)) + " descriptions out of 500")
        end = datetime.datetime.now()
        print("Time needed:" + str(end - start))
        descriptions_dao = DescriptionsDao()
        descriptions_dao.insert_description(Descriptions(descriptions_dict))
    driver.close()
    Session.close()


if __name__ == '__main__':
    offers_ids = load_offers()
    start = datetime.datetime.now()
    start_crawler(offers_ids)
    end = datetime.datetime.now()
    print("Time of whole crawling:" + str(end - start))
