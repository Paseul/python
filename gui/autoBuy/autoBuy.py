from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pyautogui
from threading import *

#로그인url
url1 = "https://login.11st.co.kr/auth/front/login.tmall?returnURL=https%3A%2F%2Fwww.11st.co.kr%2Fmain%3Fgclid%3DCj0KCQiAnb79BRDgARIsAOVbhRrxibgsWBSGunpebFEvij9z7MOpeQv4iNIikxW9Uk2AlhDw9lAYl1UaAta7EALw_wcB%26utm_term%3D11%25B9%25F8%25B0%25A1%26utm_campaign%3D%2B0810%2BPC%2B%25BA%25EA%25B7%25A3%25B5%25E5%2BK%2B%25B8%25DE%25C0%25CE%25B7%25A3%25B5%25F9%25C0%25B8%25B7%25CE%25BF%25AC%25B0%25E1%26utm_source%3D%25B1%25B8%25B1%25DB_PC_S%26utm_medium%3D%25B0%25CB%25BB%25F6"
#상품url
url2 = 'http://www.11st.co.kr/products/3167879989'
# url2 = 'http://www.11st.co.kr/products/3428070582?&trTypeCd=20&trCtgrNo=1002761'

print('페이지 로딩중...')

prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options = Options()
chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome("E:\chromedriver", options=chrome_options)
driver.maximize_window()

driver.get(url1)

#send_keys부분에 아이디를 적어주세요
driver.find_element_by_name('loginName').send_keys('machianb')
#send_keys부분에 비밀번를 적어주세요
driver.find_element_by_name('passWord').send_keys('!Phoenix7')

driver.find_element_by_class_name("btn_Atype").click()
print('로그인 완료')
driver.implicitly_wait(10)
driver.get(url2)
print('구매실행프로세스 대기중')
driver.implicitly_wait(10)
print('구매실행프로세스 작동시작')
#상품구매 반복문

while True:
    check = driver.find_element_by_class_name("dt_price")
    if check.text == '현재 판매중인 상품이 아닙니다.':
        driver.refresh()
        print("상품없음 새로고침진행...")
        driver.implicitly_wait(10)

    else:
        driver.find_element_by_class_name("buy").click()
        driver.implicitly_wait(10)
        time.sleep(0.2)
        driver.find_element_by_xpath('//*[@id="optionContainer"]/div[1]/div[1]/button').click()
        driver.implicitly_wait(10)
        time.sleep(0.2)
        driver.find_element_by_xpath('//*[@id="optlst_prdGrp"]/li[4]/a').click()
        driver.implicitly_wait(10)
        time.sleep(0.2)
        driver.find_element_by_xpath('//*[@id="optionContainer"]/div[3]/div[2]/button').click()
        driver.implicitly_wait(10)
        time.sleep(0.2)
        driver.find_element_by_xpath('//*[@id="doPaySubmit"]').click()
        driver.implicitly_wait(10)
        time.sleep(0.5)
        pyautogui.moveTo(1490, 520, 0)
        pyautogui.click()
        pyautogui.click()
        pyautogui.moveTo(1640, 520, 0)
        pyautogui.click()
        pyautogui.click()
        pyautogui.moveTo(1490, 520, 0)
        pyautogui.click()
        # pyautogui.click()
        break

