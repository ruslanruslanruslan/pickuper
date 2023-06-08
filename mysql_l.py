import mysql.connector

mydb = mysql.connector.connect(
  host="192.168.2.172",
  user="ruslan",
  password="bibonsva",
  database="tinder"
)


def insert_user(user_id, user_name, gender_id, birth_date, city, job, school, biography, zodiac_id_specified, zodiac_id_calculated, is_verified, is_online):
  mycursor = mydb.cursor()
  sql = "INSERT INTO user (id, name, gender_id, birth_date, city, job, school, biography, zodiac_id_specified, zodiac_id_calculated, is_verified, is_online) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE name = %s"
  val = (user_id, user_name, gender_id, birth_date, city, job, school, biography, zodiac_id_specified, zodiac_id_calculated, is_verified, is_online, user_name)
  mycursor.execute(sql, val)
  mydb.commit()


def insert_image(user_id, url, prob):
  mycursor = mydb.cursor()
  sql = "INSERT IGNORE INTO image (user_id, url, female_probability) VALUES (%s, %s, %s)"
  val = (user_id, url, prob)
  mycursor.execute(sql, val)
  mydb.commit()


def insert_match(id, user_id, created_date, url, is_super_like, is_super_boost_match, is_experiences_match, is_fast_match):
  mycursor = mydb.cursor()
  image_id = get_image_id(url)
  sql = "INSERT INTO pair (id, user_id, create_datetime, image_id, is_super_like, is_super_boost_match, is_experiences_match, is_fast_match) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE create_datetime = %s"
  val = (id, user_id, created_date, image_id, is_super_like, is_super_boost_match, is_experiences_match, is_fast_match, created_date)
  mycursor.execute(sql, val)
  mydb.commit()


def insert_message(message_id, match_id, create_datetime, sent_from, sent_to, message, message_plan_id):
  mycursor = mydb.cursor()
  sql = "INSERT INTO message (id, pair_id, create_datetime, sent_from, sent_to, message, message_plan_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
  val = (message_id, match_id, create_datetime, sent_from, sent_to, message, message_plan_id)
  mycursor.execute(sql, val)
  mydb.commit()


def get_image_id(url):
  mycursor = mydb.cursor()
  sql = "SELECT id FROM image WHERE url = '{}'".format(url)
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  if myresult:
    return myresult[0][0]
  else:
    return None


def check_female(user_id):
  mycursor = mydb.cursor()
  sql = "SELECT SUM(CASE WHEN (female_probability > 0.01 /*OR ABS(female_probability) < 0.02*/) THEN 1 ELSE 0 END)/COUNT(*) FROM image WHERE user_id = '{}'".format(user_id)
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  print("Good images: " + str(myresult[0][0]))
  return myresult[0][0]


def check_user_exists(user_id):
  mycursor = mydb.cursor()
  sql = "SELECT COUNT(*) FROM user WHERE id = '{}'".format(user_id)
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  if myresult[0][0] > 0:
    return True
  else:
    return False


def check_pair_exists(match_id):
  mycursor = mydb.cursor()
  sql = "SELECT COUNT(*) FROM pair WHERE id = '{}'".format(match_id)
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  if myresult[0][0] > 0:
    return True
  else:
    return False


def get_username(user_id):
  name = '(bth what is your name?)'
  mycursor = mydb.cursor()
  sql = f"SELECT IFNULL(name, '{name}') FROM user WHERE id = '{user_id}'"
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  if len(myresult) > 0:
    if myresult[0][0]:
      name = myresult[0][0]
  return name


def get_birthdate(user_id):
  mycursor = mydb.cursor()
  sql = "SELECT birth_date FROM user WHERE id = '{}'".format(user_id)
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  if len(myresult):
    if myresult[0][0]:
      return myresult[0][0]
  else:
    return None


def get_last_message_plan_id(pair_id):
  mycursor = mydb.cursor()
  sql = f"SELECT message_plan_id FROM message_plan WHERE message_plan_id = (SELECT message_plan_id FROM message WHERE create_datetime = (SELECT MAX(create_datetime) FROM message WHERE pair_id = '{pair_id}') AND pair_id = '{pair_id}')"
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  if len(myresult):
    return myresult[0][0]
  else:
    return 0


def get_next_message(last_message_plan_id, break_plan):
  mycursor = mydb.cursor()
  if break_plan:
    sql = f"SELECT message_plan_id, message_template FROM message_plan WHERE message_plan_id = (SELECT MIN(message_plan_id) FROM message_plan WHERE plan_id = 1 OR plan_id = (SELECT plan_id + 1 FROM message_plan where message_plan_id = {last_message_plan_id}))"
  else:
    sql = f"SELECT message_plan_id, message_template FROM message_plan WHERE message_plan_id = (SELECT MAX(message_plan_id) FROM message_plan WHERE message_plan_id IN (1, {last_message_plan_id} + 1))"
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  if len(myresult):
    return myresult[0]
  else:
    return None


def update_choice(user_id, choice_id):
  mycursor = mydb.cursor()
  sql = "UPDATE user SET choice_id = {} WHERE id = '{}'".format(choice_id, user_id)
  mycursor.execute(sql)
  mydb.commit()