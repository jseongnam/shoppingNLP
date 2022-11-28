from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
pages = [101, 101, 101, 71, 94, 73]
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=kr_KR')
driver = webdriver.Chrome('./chromedriver', options=options)
df_title = pd.DataFrame()    # section
url = 'https://www.lotteimall.com/display/viewDispShop.lotte?disp_no=5128912'
for i in range(1, 11):  # page
    driver.get(url)
    time.sleep(0.2)
        # btn_page = '//*[@id="cateListForm"]/fieldset[2]/div/div[4]/a[{}]'.format(i)
        # clicked_btn_page = driver.find_element('xpath', btn_page).click()
    btn_product = '//*[@id = "cateListForm"]/fieldset[2]/div/div[3]/ul/li[{}]/div[1]/a/img'.format(i)
    clicked_btn_product = driver.find_element('xpath', btn_product).click()
    driver.get(url)