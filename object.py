import datetime


class Person(object):

    def __init__(self, data, api):
        self._api = api
        self.id = data["_id"]
        self.name = data.get("name", "Unknown")
        self.bio = data.get("bio", "")
        self.distance = data.get("distance_mi", 0) / 1.60934
        self.birth_date = datetime.datetime.strptime(data["birth_date"], '%Y-%m-%dT%H:%M:%S.%fZ') if data.get("birth_date", False) else None
        self.gender = data.get("gender", 2)
        self.sexual_orientation = data['sexual_orientations'][0].get("name", "Straight") if 'sexual_orientations' in data else "Straight"
        self.images = list(map(lambda photo: photo["url"], data.get("photos", [])))
        self.jobs = list(map(lambda job: {"title": job.get("title", {}).get("name"), "company": job.get("company", {}).get("name")}, data.get("jobs", [])))
        self.schools = list(map(lambda school: school["name"], data.get("schools", [])))
        self.verified = False
        if "badges" in data:
            if "selfie_verified" in data["badges"]:
                self.verified = True
        self.city = data.get("city", {}).get("name", "Unknown")
        self.online = data.get("online_now", None)
        selected_descriptors = data.get('selected_descriptors', None)
        try:
            self.zodiac_s = self.convert_zodiac(next(item for item in selected_descriptors if item["name"] == "Zodiac")["choice_selections"][0]["name"].lower())
        except:
            self.zodiac_s = None
        try:
            self.zodiac_c = self.convert_zodiac(self.zodiac_sign(self.birth_date.day, self.birth_date.month))
        except:
            self.zodiac_c = None

    def __repr__(self):
        bd = self.birth_date or "??.??.????"
        return f"{self.id}  -  {self.name} ({self.birth_date.strftime('%d.%m.%Y') if self.birth_date is not None else '??.??.????'})"

    def like(self):
        return self._api.like(self.id)

    def dislike(self):
        return self._api.dislike(self.id)[0]["choice_selections"][0]["name"]

    def zodiac_sign(self, day, month):
        # checks month and date within the valid range
        # of a specified zodiac
        if month == 12:
            astro_sign = 'sagittarius' if (day < 22) else 'capricorn'
        elif month == 1:
            astro_sign = 'capricorn' if (day < 20) else 'aquarius'
        elif month == 2:
            astro_sign = 'aquarius' if (day < 19) else 'pisces'
        elif month == 3:
            astro_sign = 'pisces' if (day < 21) else 'aries'
        elif month == 4:
            astro_sign = 'aries' if (day < 20) else 'taurus'
        elif month == 5:
            astro_sign = 'taurus' if (day < 21) else 'gemini'
        elif month == 6:
            astro_sign = 'gemini' if (day < 21) else 'cancer'
        elif month == 7:
            astro_sign = 'cancer' if (day < 23) else 'leo'
        elif month == 8:
            astro_sign = 'leo' if (day < 23) else 'virgo'
        elif month == 9:
            astro_sign = 'virgo' if (day < 23) else 'libra'
        elif month == 10:
            astro_sign = 'libra' if (day < 23) else 'scorpio'
        elif month == 11:
            astro_sign = 'scorpio' if (day < 22) else 'sagittarius'
        return astro_sign

    def convert_zodiac(self, zodiac):
        dict = {'sagittarius':1, 'capricorn':2, 'aquarius':3, 'pisces':4, 'aries':5, 'taurus':6, 'gemini':7, 'cancer':8, 'leo':9, 'virgo':10, 'libra':11, 'scorpio':12}
        return dict[zodiac]


class Match(object):

    def __init__(self, data, api):
        self._api = api
        self.person = Person(data["person"], api)
        self.id = data["id"]
        self.user_id = data["person"]["_id"]
        self.create_datetime = datetime.datetime.strptime(data["created_date"], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.liked_img = None
        if "liked_content" in data:
            if "by_opener" in data["liked_content"]:
                if "photo" in data["liked_content"]["by_opener"]:
                    self.liked_img = data["liked_content"]["by_opener"]["photo"]["url"]
        self.is_super_like = data["is_super_like"]
        self.is_super_boost_match = data["is_super_boost_match"]
        self.is_experiences_match = data["is_experiences_match"]
        self.is_fast_match = data["is_fast_match"]
        self.message_count = data['message_count']
        self.pending = data['pending']


class Message(object):

    def __init__(self, data, api):
        self._api = api
        self.message_id = data["_id"]
        self.sent_from = data["from"]
        self.sent_to = data["to"]
        self.match_id = data["match_id"]
        self.create_datetime = datetime.datetime.strptime(data["created_date"], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.message = data["message"]
