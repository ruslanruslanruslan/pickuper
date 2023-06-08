from api import tinderAPI
from time import sleep
from datetime import date, datetime, time
from transliterate import translit
from business_duration import businessDuration
from checker import Checker
import random
import mysql_l
import traceback


# chrome_options = webdriver.ChromeOptions()
# prefs = {"profile.default_content_setting_values.notifications": 2}
# chrome_options.add_experimental_option("prefs", prefs)
# chrome_options.add_argument(r'--user-data-dir=C:\\Users\\OTHER\\AppData\\Local\\Google\\Chrome\\User Data\\')
# driver = webdriver.Chrome(options=chrome_options, executable_path="C:\\Users\\OTHER\\AppData\\Local\\Google\\Chrome\\chromedriver.exe")
# driver.get('https://tinder.com')
# custom_sleep(20)
# logs = driver.get_log("driver")
# for request in driver.requests:
#     for header in request.headers._headers:
#         if header[0] == 'x-auth-token':
#             token = header[1]
#             api = tinderAPI(token)
#             print(token)
#             driver.close()
#             break
#     if 'token' in globals():
#         break

token = "a84f7c60-fbb1-4bc7-9576-b8c0ac368cbf"
api = tinderAPI(token)


def custom_sleep(i):
    print(f"sleeping for {i} seconds")
    sleep(i)


def run_person(person):
    print("========================START PERSON==========================")
    print(str(person))
    mysql_l.insert_user(person.id, person.name, person.gender, person.birth_date, person.city,
                        next(iter(person.jobs), {}).get("title", None), next(iter(person.schools), None), person.bio,
                        person.zodiac_s, person.zodiac_c, person.verified, person.online)
    if person.verified == 1:
        api.like(person.id)
        mysql_l.update_choice(person.id, 2)
    else:
        prob_result = -1
        for img in person.images:
            prob = Checker(img)
            mysql_l.insert_image(person.id, img, prob)
            prob_result = max(prob_result, prob)
        if any(word in person.bio.lower() for word in ['trans ', 'ladyboy ', 'transwoman ']):
            api.dislike(person.id)
            mysql_l.update_choice(person.id, 1)
            print(f'It is trans!')
        elif person.sexual_orientation != 'Straight':
            print(person.sexual_orientation)
        elif any(word in person.bio.lower() for word in ['singlemom ', 'single mom ', ' mother ']):
            api.dislike(person.id)
            mysql_l.update_choice(person.id, 1)
            print(f'It RSP!')
        elif mysql_l.check_female(person.id) > 0.3:
            api.like(person.id)
            mysql_l.update_choice(person.id, 2)
            print(f'Looks like a woman')
        else:
            api.dislike(person.id)
            mysql_l.update_choice(person.id, 1)
            print(f'Looks like a man')


def prepare_user(user_id):
    if not mysql_l.check_user_exists(user_id):
        person = api.person(user_id)
        run_person(person)


def prepare_match(match_id):
    if not mysql_l.check_pair_exists(match_id):
        match = api.match(match_id)
        mysql_l.insert_match(match_id, match.user_id, match.create_datetime, match.liked_img, match.is_super_like, match.is_super_boost_match, match.is_experiences_match, match.is_fast_match)


def send_message(match_id, user_id, message_template):
    birthdate = mysql_l.get_birthdate(user_id)
    today = date.today()
    age = 0
    if birthdate:
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    name = mysql_l.get_username(user_id)
    # try:
    #     name = translit(name, "ru")
    # except:
    #     name = ""
    # message_text = f"Hi {name} :)"
    message_text = message_template[1].replace("{nickname}", name)
    print(f'Send to {name} ({user_id}) "{message_text}"')
    message = api.message_send(match_id, message_text)
    prepare_user(message.sent_from)
    mysql_l.insert_message(message.message_id, message.match_id, message.create_datetime, message.sent_from, message.sent_to, message.message, message_template[0])
    api.message_watch(match_id, message.message_id)
    custom_sleep(random.randint(5, 20))


for i in range(1000):

    try:

        print("=============================================================")
        print("=====================START OLD MESSAGE=======================")
        print("=============================================================")
        chats = api.chats()
        c = 0
        for chat in chats:
            c += 1
            print(f'=========={str(c)}. {chat["user_name"]} ({chat["match_id"]}, {chat["user_id"]})==========')
            prepare_user(chat['user_id'])
            prepare_match(chat['match_id'])
            messages = api.message_list(chat['match_id'])
            last_date = chat['last_message_datetime'] if chat['last_message_datetime'] != None else chat['created_date']
            last_msg_delay = businessDuration(last_date, datetime.utcnow(), starttime=time(7,0,0),endtime=time(22,0,0), weekendlist=[])
            bot_last_message_plan_id = mysql_l.get_last_message_plan_id(chat['match_id'])
            last_message_from = messages[0]['from'] if len(messages) > 0 else chat['user_id']
            last_message_text = messages[0]["message"] if len(messages) > 0 else '(Just gave a like)'
            if last_message_from == chat['user_id']:  # если ответила
                print(f'She sent new message : "{last_message_text}"')
                if len(messages) > 1:
                    msg_interval = min(divmod(abs(datetime.strptime(messages[0]['created_date'], '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.strptime(messages[1]['created_date'], '%Y-%m-%dT%H:%M:%S.%fZ')).total_seconds(), 60)[0], 24 * 60)
                else:
                    msg_interval = 0
                print(f'Im waiting already {last_msg_delay} minutes and need to wait {msg_interval} minutes')
                if last_msg_delay > msg_interval: # если прошло соответствующее ее темпам время
                    bot_next_message = mysql_l.get_next_message(bot_last_message_plan_id, False)
                    send_message(chat['match_id'], chat['user_id'], bot_next_message)
            elif last_msg_delay > 60 * 1 * 24: # если молчит более суток
                print(f'She not answer for {last_msg_delay} minutes')
                person = api.person(chat['user_id'])
                print(f'Im in {person.distance} miles')
                bot_next_message = mysql_l.get_next_message(bot_last_message_plan_id, True)
                if person.distance < 30:
                    send_message(chat['match_id'], chat['user_id'], bot_next_message)
                elif last_msg_delay > 60 * 3 * 24:
                    print(f'Anyway too long without contact')
                    send_message(chat['match_id'], chat['user_id'], bot_next_message)
                    if len(messages) > 30: #удаляем если затянулась переписка и молчит
                        api.unmatch(chat['match_id'])
                    elif len(messages) > 4:
                        if messages[0]['to'] == messages[1]['to'] == messages[2]['to'] == messages[3]['to'] == chat['user_id']:
                            api.unmatch(chat['match_id'])
                else:
                    print(f'Last message was only {last_msg_delay/60} hours ago and distance is {person.distance}')
            else:
                print(f'Last message was only {last_msg_delay/60} hours ago')
            print()

        print ("=============================================================")
        print ("=====================START NEW MESSAGE=======================")
        print ("=============================================================")
        matches = api.matches()
        for match in matches:
            prepare_user(match.user_id)
            prepare_match(match.id)
            if len(api.message_list(match.id)) == 0:
                bot_next_message = mysql_l.get_next_message(0, False)
                send_message(match.id, match.user_id, bot_next_message)

        # print ("=============================================================")
        # print ("========================START BATCH==========================")
        # print ("=============================================================")
        # persons = api.nearby_persons()
        # if not persons == None:
        #     for person in persons:
        #         run_person(person)
        #         custom_sleep(random.randint(10, 50))
        # else:
        #     print('Nobody found')

        custom_sleep(random.randint(50, 200))

    except:
        traceback.print_exc()
        custom_sleep(random.randint(50, 200))
        pass


# last_message = api.message_list("5e0fa84033986c0100903e395ff36a6f8dc2df0100869e87")[0]["_id"]
# message = api.message_watch("5e0fa84033986c0100903e395ff36a6f8dc2df0100869e87", last_message)
