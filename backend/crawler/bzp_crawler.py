from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from scrapy.selector import Selector
import json
import os

data = []


def scrape_offers():
    i = 1
    while True:
        try:
            site_changed_xpath = \
                '//b[@class="dxp-lead dxp-summary" and contains(text(), "Strona ' + str(i) + ' z 500 (elementy 5000)")]'
            print(site_changed_xpath)
            WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, site_changed_xpath)))
            next_xpath = '//a[@class="dxp-button dxp-bi" and child::img[@alt="Następna"]]'
            next = driver.find_element_by_xpath(next_xpath)
            html = driver.page_source

            rows = Selector(text=html).css('tr.dxgvDataRow_Aqua')

            for row in rows:
                data.append({row.css("td.dxgv::text")[1].extract(): row.css("td.dxgv::text")[6].extract()})

            next.click()
            i += 1
            print(i)
        except Exception as e:
            print(e)
            break


if __name__ == '__main__':
    # driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'))
    driver = webdriver.Chrome()
    driver.get('https://searchbzp.uzp.gov.pl/Search.aspx')

    scrape_offers()

    old = driver.find_element_by_id('ctl00_ContentPlaceHolder1_rbBZP_Old')
    old.click()
    time.sleep(20)

    search = driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnSearch')
    search.click()
    time.sleep(20)

    first = driver.find_element_by_xpath('//a[contains(text(), "1")]')
    first.click()
    time.sleep(20)

    scrape_offers()

    with open("description.json", "a") as json_file:
        json.dump(data, json_file)
    driver.close()
