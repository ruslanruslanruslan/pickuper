from api import tinderAPI
from time import sleep
from datetime import date
from datetime import datetime
from transliterate import translit
from checker import Checker
import random
import mysql_l
import tinder_token
from tinder_token.facebook import TinderTokenFacebookV2
# from selenium import webdriver
# import chromedriver
from seleniumwire import webdriver

# facebook = TinderTokenFacebookV2()
# token = facebook.get_tinder_token(fb_email='r.r.ibragimov@yandex.ru', fb_password='BibonsvA91')[0]
# api = tinderAPI(token)

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument(r'--user-data-dir=C:\\Users\\OTHER\\AppData\\Local\\Google\\Chrome\\User Data\\')
driver = webdriver.Chrome(options=chrome_options, executable_path="C:\\Users\\OTHER\\AppData\\Local\\Google\\Chrome\\chromedriver.exe")
driver.get('https://tinder.com')
sleep(20)
for request in driver.requests:
    for header in request.headers._headers:
        if header[0] == 'x-auth-token':
            token = header[1]
            api = tinderAPI(token)
            print(token)
            driver.close()
            break
    if 'token' in globals():
        break


# token = "c20839ec-6b4d-445e-93fc-ba136baf1418"
# api = tinderAPI(token)


def generate_message_text(user_id):
    birthdate = mysql_l.get_birthdate(user_id)
    today = date.today()
    age = 0
    if birthdate:
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    name = mysql_l.get_username(user_id)
    try:
        name = translit(name, "ru")
    except:
        name = ""
    message_text = f"Привет {name} :)"
    if age > 36:
        message_text = f"Доброго Вам дня, {name} 🙇"
    return message_text


    print ("=============================================================")
    print ("========================START MESSAGE==========================")
    print ("=============================================================")
    chats = api.chats()
    for chat in chats:
        last_msg_delay = abs((datetime.now() - chat['last_message_datetime']).days)
        if last_msg_delay > 3:
            message_text = generate_message_text(chat['user_id'])
            print(f'Send to {chat["user_id"]} "{message_text}"')
            message = api.message_send(chat['match_id'], message_text)
            sleep(random.randint(0, 10))
            mysql_l.insert_message(message.message_id, message.match_id, message.create_datetime, message.sent_from, message.sent_to, message.message)
        else:
            print(f'Last message to {chat["user_id"]} was only {last_msg_delay} days ago')
        sleep(random.randint(10, 50))
