# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 17:25:34 2019
@主題:中央大學人資系統自動簽到程式
@作者: Ming a.k.a 神奇寶貝訓練家
@實作方式:以腳本方式結合Chrome進行自動簽到

@系統需求:需先pip install selenium 、以及下載符合版本的ChromeDriver(下載點:http://chromedriver.chromium.org/downloads)
@需求:[使用者帳號]、[使用者密碼]、[工作事項]
"""
'''
黃展皇自行變更：
1. chromedriver_autoinstaller模組(需先pip install chromedriver_autoinstaller), 可無須下載ChromeDriver
可自行windows排程
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from auto_signInOut_IDPW import ID, PW #我自己的帳密，才不給你看咧
import chromedriver_autoinstaller
import time
chromedriver_autoinstaller.install()

#可在此輸入帳號密碼
###需求:[使用者帳號]
userName= (ID)
###需求:[使用者密碼]
userPass= (PW)
###需求:[自己f12看簽到退的按鈕的ID是多少]
sign_element_id_list = ['SignOut_10714']

#開瀏覽器輸入帳密並登入
driver = webdriver.Chrome()
driver.get('https://imo.3t.org.tw/Login')
##driver.set_window_position(0,0) #瀏覽器位置
userName_element = driver.find_element(By.NAME, 'ID')
userName_element.send_keys(userName)
userPass_element = driver.find_element(By.NAME, 'PW')
userPass_element.send_keys(userPass)
button = driver.find_element(By.NAME, 'Btn')
button.click()

#進入任務追蹤頁面依序按簽到退(這瀏覽器剛開剛登入應該不會有連線逾時而要重新打帳密的問題)
driver.get('https://imo.3t.org.tw/FActive/Index/2756') #每個人都一樣?
for sign_element_id in sign_element_id_list:
    sign_element = driver.find_element(By.ID, sign_element_id)
    sign_element.click()
    sure_element = driver.find_element(By.CLASS_NAME, 'is-premary')
    sure_element.click()
    gobackgoback_element = driver.find_element(By.CLASS_NAME, 'btn is-premary is-go')
    gobackgoback_element.click()
print('done!!')

time.sleep(30)
driver.close()

# TODO: 1. 防'網站防機器人/Dos攻擊'的亂數時間模糊
#       2. 自動蒐集活動時機，接近就簽到退