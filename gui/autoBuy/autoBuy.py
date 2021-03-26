# 2020-11-15

# License
# 11buy.py파일을 수정 배포 가능하나 11buy.py을 가지고 수익을 발생하면 민형사상 법적 처벌을 받을 수 있습니다.
# 수정 배포 시 원작자의 주소를 남겨주세요
# 제작자 : https://little-pig.tistory.com/
# 원문 : https://little-pig.tistory.com/entry/11%EB%B2%88%EA%B0%80-%EB%A7%A4%ED%81%AC%EB%A1%9C%EC%98%A4%ED%86%A0%EB%A7%A4%ED%81%AC%EB%A1%9Cselenium%EC%9E%90%EB%8F%99%EA%B5%AC%EB%A7%A4%EC%98%88%EC%95%BD%EA%B5%AC%EB%A7%A4

from selenium import webdriver
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#로그인url
url1 = "https://login.11st.co.kr/auth/front/login.tmall?returnURL=https%3A%2F%2Fwww.11st.co.kr%2Fmain%3Fgclid%3DCj0KCQiAnb79BRDgARIsAOVbhRrxibgsWBSGunpebFEvij9z7MOpeQv4iNIikxW9Uk2AlhDw9lAYl1UaAta7EALw_wcB%26utm_term%3D11%25B9%25F8%25B0%25A1%26utm_campaign%3D%2B0810%2BPC%2B%25BA%25EA%25B7%25A3%25B5%25E5%2BK%2B%25B8%25DE%25C0%25CE%25B7%25A3%25B5%25F9%25C0%25B8%25B7%25CE%25BF%25AC%25B0%25E1%26utm_source%3D%25B1%25B8%25B1%25DB_PC_S%26utm_medium%3D%25B0%25CB%25BB%25F6"
#상품url
# url2 = 'http://www.11st.co.kr/products/3167879989?trTypeCd=03&trCtgrNo=2050639'
url2 = 'http://www.11st.co.kr/products/3326702930?trTypeCd=03&trCtgrNo=2051889'


print('페이지 로딩중...')

#크롬다르이버 다운로드 주소입니다.
# driver = webdriver.Chrome("/usr/local/bin/chromedriver")
mobile_emulation = { "deviceName": "iPhone X" }
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver", options=chrome_options)

driver.get(url1)

#send_keys부분에 아이디를 적어주세요
driver.find_element_by_name('loginName').send_keys('machianb')
#send_keys부분에 비밀번를 적어주세요
driver.find_element_by_name('passWord').send_keys('!Phoenix7')

login = driver.find_element_by_class_name("btn_Atype")
login.click()
print('로그인 완료')

driver.get(url2)
print('구매실행프로세스 대기중')
time.sleep(1)
print('구매실행프로세스 작동시작')
#상품구매 반복문
while True:
    check = driver.find_element_by_class_name("dt_price")
    if check.text == '현재 판매중인 상품이 아닙니다.':
        driver.refresh()
        print("상품없음 새로고침진행...")
        driver.implicitly_wait(10)

    else:
        buy = driver.find_element_by_class_name("buy")
        buy.click()
        opt = driver.find_element_by_class_name("opt_lists")
        print(driver.find_elements_by_css_selector('button.select_opt'))

        break
time.sleep(2)

#결제 시스템 부분
print("일반결제...")
radio=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//input[@id='payOthers']/following::span[1]")))
driver.execute_script("arguments[0].click();", radio)
# noaccount_table = driver.find_element_by_id("paymentGeneralTab5")
# print("무통장입금 선택")
# noaccount_table.click()
# bankKindCtl = driver.find_element_by_id("bankKindCtl04")
# bankKindCtl.click()
# buying = driver.find_element_by_class_name("btn_order")
# buying.click()
# print("주문이 완료되었습니다.")
