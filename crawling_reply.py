from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime
from selenium.webdriver.common.keys import Keys

category = []
pages = []


options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=kr_KR')
driver = webdriver.Chrome('./chromedriver', options=options)
df_reply = pd.DataFrame()
replys = []

for i in range(1, 2):  # page_count
    url = 'https://www.ssg.com/disp/category.ssg?ctgId=6000092898&page={}'.format(i) #우유 url
    driver.get(url)
    for j in range(1, 2): # product_count
        #product 클릭
        try:
            time.sleep(0.5)
            btn_product = '//*[@id="ty_thmb_view"]/ul/li[{}]/div[2]/div[2]/div/a'.format(j) #제품 xpath
            clicked_btn_product = driver.find_element('xpath', btn_product).send_keys(Keys.ENTER)

        except NoSuchElementException as e:
            try:
                time.sleep(0.5)
                btn_product = '//*[@id="ty_thmb_view"]/ul/li[{}]/div[2]/div[2]/div/a/em[1]'.format(j)   #제품 xpath
                clicked_btn_product = driver.find_element('xpath', btn_product).send_keys(Keys.ENTER)
                time.sleep(1)
            except:
                print('none')

        for k in range (1, 10):
            try:
                time.sleep(0.5)
                btn_reply = '//*[@id="comment_navi_area"]/a[{}]'.format(k)  #k번째 제품들 xpath
                clicked_btn_reply = driver.find_element('xpath', btn_reply).send_keys(Keys.ENTER)
                for l in range(1, 20, 2):
                    try:
                        reply = '//*[@id="cdtl_cmt_tbody"]/tr[{}]/td[1]/div/a/div[1]/span'.format(l)    #댓글 xpath
                        reply = driver.find_element('xpath', reply).text
                        print(reply)
                        reply = re.compile('[^가-힣]').sub(' ', reply)
                        replys.append(reply)

                    except NoSuchElementException as e:
                        print('none')
            except StaleElementReferenceException as r:
                print('none')

            except NoSuchElementException as e:
                print('none')

        driver.back()
        time.sleep(3)

if i % 1 == 0:
    df_section_reply = pd.DataFrame(replys, columns=['reply'])
    df_section_reply['category'] = 'Dairy'
    df_title = pd.concat([df_reply, df_section_reply], ignore_index=True)
    df_title.to_csv('./crawling_data/crawling_data_{}_To_{}.csv'.format(i, j),
                            index = False)
    replys = []




# btn_product = '//*[@id="ty_thmb_view"]/ul/li[16]/div[2]/div[2]/div/a/em[1]'
#//*[@id="cdtl_cmt_tbody"]/tr[1]/td[1]/div/a/div[1]/span
