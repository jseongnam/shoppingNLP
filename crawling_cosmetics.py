from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

category = ['kids','book','refresh','sports']



options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=kr_KR')
options.add_argument("--disable-popup-blocking")
driver = webdriver.Chrome('./chromedriver', options=options)
df_reply = pd.DataFrame()
replys = []
urls = ['https://www.ssg.com/disp/category.ssg?dispCtgId=6000161215&page=',
        'https://www.ssg.com/disp/category.ssg?dispCtgId=6000210206&page=',
        'https://www.ssg.com/disp/category.ssg?dispCtgId=6000092893&page=',
        'https://www.ssg.com/disp/category.ssg?dispCtgId=6000204818&page=']

for i in range(len(urls)):  # url
    for k in range(1,4):   #page
        url = urls[i]+str(k)
        print("url:",url)
        driver.get(url)
        for j in range(1, 81): # product_count
            #product 클릭
            try:
                time.sleep(0.5)
                btn_product = '//*[@id="ty_thmb_view"]/ul/li[{}]/div[2]/div[2]/div/a'.format(j) #제품 xpath
                clicked_btn_product = driver.find_element('xpath', btn_product).send_keys(Keys.ENTER)

                try : # 에러창이 나올 시, 3초 기다리고 에러창 끈 후에 이전 URL로 이동
                    WebDriverWait(driver, 3).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    time.sleep(1)
                    driver.get(url)
                    pass

                except: # 에러창 없을 시, 코드 계속 진행
                    continue
            except NoSuchElementException as e:
                try:
                    time.sleep(0.5)
                    btn_product = '//*[@id="ty_thmb_view"]/ul/li[{}]/div[2]/div[2]/div/a/em[1]'.format(j)   #제품 xpath
                    clicked_btn_product = driver.find_element('xpath', btn_product).send_keys(Keys.ENTER)
                    time.sleep(1)

                    try:  # 에러창이 나올 시, 3초 기다리고 에러창 끈 후에 이전 URL로 이동
                        WebDriverWait(driver, 3).until(EC.alert_is_present())
                        alert = driver.switch_to.alert
                        alert.accept()
                        time.sleep(1)
                        driver.get(url)
                        pass

                    except:  # 에러창 없을 시, 코드 계속 진행
                        continue
                except:
                    print('none')
                for t in range(1, 10):
                    try:
                        time.sleep(0.5)
                        btn_reply = '//*[@id="comment_navi_area"]/a[{}]'.format(t)  # k번째 리뷰 버튼 xpath
                        clicked_btn_reply = driver.find_element('xpath', btn_reply).send_keys(Keys.ENTER)
                        for l in range(1, 20, 2):
                            try:
                                reply = '//*[@id="cdtl_cmt_tbody"]/tr[{}]/td[1]/div/a/div[1]/span'.format(l)    #댓글 xpath
                                reply = driver.find_element('xpath', reply).text
                                print(reply)
                                reply = re.compile('[^가-힣]').sub(' ', reply)
                                replys.append(reply)
                                time.sleep(0.5)
                            except NoSuchElementException as e:
                                print('none')
                    except StaleElementReferenceException as r:
                        print('none')

                    except NoSuchElementException as e:
                        print('none')

            driver.back()
            time.sleep(3)

        if k % 1 == 0 :#3번째마다 저장
            df_section_reply = pd.DataFrame(replys, columns=['reply'])
            df_section_reply['category'] = category[i]
            df_title = pd.concat([df_reply, df_section_reply], ignore_index=True)
            df_title.to_csv('./crawling_data/crawling_data_{}_To_{}.csv'.format(category[i],k),
                                            index = False)
            replys = []
            print('debug01',k)
            break




# btn_product = '//*[@id="ty_thmb_view"]/ul/li[16]/div[2]/div[2]/div/a/em[1]'
#//*[@id="cdtl_cmt_tbody"]/tr[1]/td[1]/div/a/div[1]/span