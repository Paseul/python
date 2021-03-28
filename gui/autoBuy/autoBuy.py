from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pyautogui
from threading import *

#로그인url
url1 = "https://login.11st.co.kr/auth/front/login.tmall?returnURL=https%3A%2F%2Fwww.11st.co.kr%2Fmain%3Fgclid%3DCj0KCQiAnb79BRDgARIsAOVbhRrxibgsWBSGunpebFEvij9z7MOpeQv4iNIikxW9Uk2AlhDw9lAYl1UaAta7EALw_wcB%26utm_term%3D11%25B9%25F8%25B0%25A1%26utm_campaign%3D%2B0810%2BPC%2B%25BA%25EA%25B7%25A3%25B5%25E5%2BK%2B%25B8%25DE%25C0%25CE%25B7%25A3%25B5%25F9%25C0%25B8%25B7%25CE%25BF%25AC%25B0%25E1%26utm_source%3D%25B1%25B8%25B1%25DB_PC_S%26utm_medium%3D%25B0%25CB%25BB%25F6"
#상품url
url2 = 'http://www.11st.co.kr/products/3167879989?trTypeCd=03&trCtgrNo=2050639'
# url2 = 'http://www.11st.co.kr/products/3326702930?trTypeCd=03&trCtgrNo=2051889'
url3 = 'https://buy.11st.co.kr/cart/CartAction.tmall?method=getCartList'

print('페이지 로딩중...')

mobile_emulation = { "deviceName": "Galaxy S5" }
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
chrome_options.add_experimental_option("prefs", prefs)
chrome_options2 = webdriver.ChromeOptions()
chrome_options2.add_experimental_option("prefs", prefs)
# driver = webdriver.Chrome("/home/jh/chromedriver", options=chrome_options)
# driver2 = webdriver.Chrome("/home/jh/chromedriver")
driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver", options=chrome_options)
driver2 = webdriver.Chrome("C:\chromedriver_win32\chromedriver", options=chrome_options2)
driver2.maximize_window()

driver.get(url1)
driver2.get(url1)

#send_keys부분에 아이디를 적어주세요
driver.find_element_by_name('loginName').send_keys('starbgh123')
driver2.find_element_by_name('loginName').send_keys('starbgh123')
#send_keys부분에 비밀번를 적어주세요
driver.find_element_by_name('passWord').send_keys('wlgP7942')
driver2.find_element_by_name('passWord').send_keys('wlgP7942')

driver.find_element_by_class_name("btn_Atype").click()
driver2.find_element_by_class_name("btn_Atype").click()
print('로그인 완료')
driver.implicitly_wait(10)
driver2.implicitly_wait(10)
driver.get(url2)
driver2.get(url3)
print('구매실행프로세스 대기중')
driver.implicitly_wait(10)
driver2.implicitly_wait(10)
print('구매실행프로세스 작동시작')
#상품구매 반복문


def order(driver):
    print("order_t")
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
            # print(opt.find)
            driver.find_element_by_xpath('//*[@id="optionContainer"]/div[1]/div[1]/button').send_keys(Keys.ENTER)
            driver.implicitly_wait(10)
            driver.find_element_by_xpath('//*[@id="optlst_0"]/li[1]/a/span[2]').click()
            driver.implicitly_wait(10)
            driver.find_element_by_xpath('//*[@id="basketButton"]').click()
            break

order_t = Thread(target=order, args=(driver,))
order_t.daemon = True
order_t.start()

while True:
    check = driver2.find_element_by_class_name("c_order_cart_list")
    if check.text == '장바구니에 담긴 상품이 없습니다.':
        driver2.refresh()
        print("상품없음 새로고침진행...")
        driver2.implicitly_wait(10)

    else:
        driver2.find_element_by_xpath('//*[@id="doOrderBt"]').click()
        driver2.implicitly_wait(10)

        driver2.find_element_by_xpath('//*[@id="btnAccount"]').click()
        driver2.implicitly_wait(10)
        time.sleep(1)
        pyautogui.moveTo(830, 710, 0)
        pyautogui.click()
        pyautogui.click()
        pyautogui.moveTo(910, 710, 0)
        pyautogui.click()
        pyautogui.click()
        pyautogui.moveTo(830, 710, 0)
        pyautogui.click()
        pyautogui.click()
        break
