import requests,json,time
import urllib.parse
import configparser
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="114.0.5735.90").install()), options=options)
driver.implicitly_wait(10)

# 인원
adult='2'
# 구간
pathDate='SEL-CJU-20230928' # CJU:제주 , GMP:김포

flighturl = 'https://m-flight.naver.com/flights/domestic/'+pathDate+'?adult='+adult+'&isDirect=true&fareType=YC'
ticket = False
rCnt = 0

msg = MIMEText('항공권 확인 : ' + flighturl)
msg['Subject'] = '테스트'
msg['From'] = 'silentjin@mocomsys.com'
msg['To'] = 'silentjini@gmail.com'

smtp = smtplib.SMTP('ezsmtp.bizmeka.com', 587)
smtp.ehlo()      # say Hello
smtp.starttls()  # TLS 사용시 필요
smtp.login('silentjin@mocomsys.com', 'wlsl1qa@WS')
smtp.sendmail('silentjin@mocomsys.com', 'silentjini@gmail.com', msg.as_string())

while True:
    driver.get(flighturl)
    # 항공편 없음 - <div class="noResult_NoResult__2TDfz">
    try:
        element = driver.find_element(By.CLASS_NAME,'noResult_NoResult__2TDfz')
        print("No Ticket!!")
    except NoSuchElementException:
        print("There are Ticket!!")        
        smtp = smtplib.SMTP('ezsmtp.bizmeka.com', 587)
        smtp.ehlo()      # say Hello
        smtp.starttls()  # TLS 사용시 필요
        smtp.login('silentjin@mocomsys.com', 'wlsl1qa@WS')
        smtp.sendmail('silentjin@mocomsys.com', 'silentjini@gmail.com', msg.as_string())
        time.sleep(600)
    
    time.sleep(10)
