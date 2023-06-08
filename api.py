import requests
from object import Person
from object import Match
from object import Message
from datetime import datetime

TINDER_URL = "https://api.gotinder.com"


class tinderAPI():

    def __init__(self, token):
        self._token = token

    # def profile(self):
    #     data = requests.get(TINDER_URL + "/v2/profile?include=account%2Cuser", headers={"X-Auth-Token": self._token}).json()
    #     # return Profile(data["data"], self)
    #     return data["data"]

    def matches(self, limit=100):
        data = requests.get(TINDER_URL + f"/v2/matches?count={limit}", headers={"X-Auth-Token": self._token})
        data = data.json()
        match_out = []
        for match in data["data"]["matches"]:
            if match["seen"]["match_seen"] == False:
                match_out.append(Match(match, self))
        return match_out

    def chats_pack(self, match_list):
        match_out = []
        for match in match_list:
            # if match["seen"]["match_seen"] == True:


            obj = {"match_id": match['_id'],
                   "user_id": match['person']['_id'],
                   "user_name": match['person']['name'],
                   "last_message_datetime": datetime.strptime(match['messages'][0]['sent_date'], '%Y-%m-%dT%H:%M:%S.%fZ') if len(match['messages']) > 0 else None,
                   "match_seen": match['seen']['match_seen'],
                   "pending": match['pending'],
                   "created_date": datetime.strptime(match['created_date'], '%Y-%m-%dT%H:%M:%S.%fZ')}
            match_out.append(obj)
        return match_out
    def chats(self, limit=10):
        data = requests.get(TINDER_URL + f"/v2/matches?count={limit}", headers={"X-Auth-Token": self._token}).json()
        match_out = []
        match_out += self.chats_pack(data["data"]["matches"])
        next_page_token = data["data"]["next_page_token"] if "next_page_token" in data["data"] else None
        while next_page_token:
            data = requests.get(TINDER_URL + f"/v2/matches?count={limit}&page_token={next_page_token}", headers={"X-Auth-Token": self._token}).json()
            match_out += self.chats_pack(data["data"]["matches"])
            next_page_token = data["data"]["next_page_token"] if "next_page_token" in data["data"] else None
        return match_out

    def like(self, user_id):
        print("LIKE!")
        data = requests.get(TINDER_URL + f"/like/{user_id}", headers={"X-Auth-Token": self._token}).json()
        return {
            "is_match": data["match"],
            "liked_remaining": data["likes_remaining"]
        }

    def dislike(self, user_id):
        print("DISLIKE!")
        requests.get(TINDER_URL + f"/pass/{user_id}", headers={"X-Auth-Token": self._token}).json()
        return True

    def unmatch(self, match_id):
        requests.delete(TINDER_URL + f"/user/matches/{match_id}", headers={"X-Auth-Token": self._token}).json()
        return True

    def nearby_persons(self):
        data = requests.get(TINDER_URL + "/v2/recs/core", headers={"X-Auth-Token": self._token}).json()
        if "results" in data["data"]:
            return list(map(lambda user: Person(user["user"], self), data["data"]["results"]))
        else:
            return None

    def match(self, match_id):
        data = requests.get(TINDER_URL + f"/v2/matches/{match_id}", headers={"X-Auth-Token": self._token}).json()
        return Match(data['data'], self)

    def person(self, user_id):
        data = requests.get(TINDER_URL + f"/user/{user_id}", headers={"X-Auth-Token": self._token}).json()
        return Person(data["results"], self)

    def message_send(self, match_id, message):
        data = requests.post(TINDER_URL + f"/user/matches/{match_id}", headers={"X-Auth-Token": self._token}, data={"message": message}).json()
        return Message(data, self)

    def message_list(self, match_id, limit=200):
        data = requests.get(TINDER_URL + f"/v2/matches/{match_id}/messages?count={limit}", headers={"X-Auth-Token": self._token}).json()
        return data["data"]["messages"]

    def message_watch(self, match_id, message_id):
        data = requests.post(TINDER_URL + f"/v2/seen/{match_id}/{message_id}", headers={"X-Auth-Token": self._token}).json()
        return data["meta"]

