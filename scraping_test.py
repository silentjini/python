import requests,json,time
import urllib.parse
import configparser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.common.exceptions import NoSuchElementException

# KAKAO API Config
properties = configparser.ConfigParser()  
properties.read('./properties/api.dat')
kakao=properties["KAKAO"]

print(kakao["client_id"])
print(kakao["client_secret"])

properties.set("KAKAO", "client_id", "AAAA")
print(kakao["client_id"])

with open('./properties/api.dat', "w") as f:
    properties.write(f)
f.close()

exit()

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(10)


# 인원
adult='2'
# 구간
pathDate='CJU-GMP-20220508' # CJU:제주 , GMP:김포

flighturl = 'https://m-flight.naver.com/flights/domestic/'+pathDate+'?adult='+adult+'&isDirect=true&fareType=YC'
ticket = False
rCnt = 0

while True:
    driver.get(flighturl)
    # 항공편 없음 - <div class="noResult_NoResult__2TDfz">
    try:
        element = driver.find_element(By.CLASS_NAME,'noResult_NoResult__2TDfz')
        print("No Ticket!!")
    except NoSuchElementException:
        print("There are Ticket!!")
    
    time.sleep(10)
