import requests,json,time
import configparser
import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# KAKAO API Config
api_property_path='./properties/api.dat'
properties = configparser.ConfigParser()
properties.read(api_property_path)
kakao=properties["KAKAO"]

client_id = kakao["client_id"]
client_secret = kakao["client_secret"]
redirect_url = kakao["redirect_url"]

# 인증 코드로 메세지 전송 토큰 발급
tokenUrl = 'https://kauth.kakao.com/oauth/token'

data = {
    "grant_type":"authorization_code",
    "client_id": client_id,
    "client_secret": client_secret,
    "redirect_uri": redirect_url,
    "code": "HBLEIJt_csvvYXMjjSb0h88GcpF-pbLWlMtcTy11YPPDzIjtxO1H80v9IgPBJmMqUqzJQAo9dJkAAAGAjNPEog",
    }
response = requests.post(tokenUrl, data=data)
tokens = response.json()
print(tokens)

properties.set("KAKAO", "access_token", tokens["access_token"])
properties.set("KAKAO", "refresh_token", tokens["refresh_token"])
with open(api_property_path, "w") as f:
    properties.write(f)

access_token = kakao["access_token"]
refresh_token = kakao["refresh_token"]

# 친구 목록 가져오기 
friendsUrl = "https://kapi.kakao.com/v1/api/talk/friends?limit=10"
headers = { "Authorization" : "Bearer " + access_token }
response=requests.get(friendsUrl,headers=headers)
friends = response.json()
print(friends)  

# 카카오 친구 UUID eUt-S3lJfkx4VGFYbVtuXG9eckV2TnxOdhs, eUt4SHxIcERwQ29cZFZiUGRVZlZ6TX5GdEZ-Gw
friends_uuid = kakao["friends_uuid"]
uuidData=[friends_uuid]

# 테스트 메세지 발송
messageUrl="https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
memoUrl="https://kapi.kakao.com/v2/api/talk/memo/default/send"
data={    
        "receiver_uuids": json.dumps(uuidData),
        "template_object": json.dumps({
            "object_type": "text",\
            "text": "테스트 메세지!!",\
            "link": {"web_url": "https://developers.kakao.com",\
                    "mobile_web_url": "https://developers.kakao.com"},\
            "button_title": "바로 확인"
        })
    }
headers = { "Authorization" : "Bearer " + access_token }

res=requests.post(messageUrl,data=data,headers=headers)
print(res.json())
print(res.status_code)
res=requests.post(memoUrl,data=data,headers=headers)
print(res.json())
print(res.status_code)

# 크롬 웹드라이버 실행
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(10)

# 인원
adult='2'
# 구간
pathDate='SEL-CJU-20230929' # CJU:제주 , GMP:김포
flightUrl = 'https://m-flight.naver.com/flights/domestic/'+pathDate+'?adult='+adult+'&isDirect=true&fareType=YC'
ticket = False
rCnt = 0

while True:
    d = datetime.datetime.now()
    print (d)
    rCnt += 1
    if(rCnt%100 == 0):        
        # access_token 재발급
        url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token
        }
        response = requests.post(url, data=data)
        tokens = response.json()        
        print(tokens)
        access_token = tokens["access_token"]
        rCnt = 0

        properties.set("KAKAO", "access_token", access_token)
        with open(api_property_path, "w") as f:
            properties.write(f)

    driver.get(flightUrl)
    try:        
        # 항공편 없음 - <div class="noResult_NoResult__2TDfz">
        element = driver.find_element(By.CLASS_NAME,'noResult_NoResult__2TDfz')
        print("No Ticket!!")
        ticket = False
    except NoSuchElementException:
        print("There are Ticket!!")
        if not ticket:
            print("Send to Kakao..")
            ticket = True
            data={
                    "receiver_uuids": json.dumps(uuidData),
                    "template_object": json.dumps({
                        "object_type": "text",\
                        "text": "항공권 확인!!\n" + flightUrl,\
                        "link": {"web_url": "https://developers.kakao.com",\
                                "mobile_web_url": "https://developers.kakao.com"},\
                        "button_title": "바로 확인"
                    })
                }
            headers = { "Content-Type" : "application/x-www-form-urlencoded",\
                        "Authorization" : "Bearer " + access_token }
            res=requests.post(messageUrl,data=data,headers=headers)
            print(res.json())
            print(res.status_code)
            res=requests.post(memoUrl,data=data,headers=headers)
            print(res.json())
            print(res.status_code)
        else:
            print("But not send to Kakao...")
            ticket = True
    time.sleep(10)
