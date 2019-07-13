import json
import urllib.request
import re
from my_token import main_token, tokens


class Loader:

    def __init__(self,db_driver):
        self.__db_driver = db_driver
        pass

    def __vk_request(self,method, params, token):
        url = f"https://api.vk.com/method/{method}?{params}&access_token={token}&v=5.92"
        response = urllib.request.urlopen(url)
        return json.loads(response.read().decode('utf8'))

    def __get_items(self,json_object):
        if ('response' in json_object):
            if ( json_object['response'] is not None and 'items' in json_object['response']):
                return json_object['response']['items']
            else:
                return json_object['response']
        else:
            return None

    def __get_friends(self,users):
        friends = {}
        ids = [user['id'] for user in users]
        i=0
        while i < len(ids):
            items = []
            for token in tokens:
                params = re.sub('[\s\[\]]','',f"user_ids={ids[i:i+25]}")
                res = self.__vk_request('execute.myGetFriends', params, token)
                items += self.__get_items(res)
                # if 'execute_errors' in res:
                #     print(res['execute_errors'])
                i+=25
                if i >= len(ids):
                    break
            for item in items:
                friends[item['user_id']] = item['friends_ids']
        return friends


    def download_data_from_vk(self):
        # res = self.__vk_request('users.search', 'university=1088')
        # print(res)
        ids = set()
        for age in range(10, 100):
            res = self.__vk_request('users.search', f'age_from={age}&age_to={age + 1}&university=1088&count=1000',main_token)
            # users cleaning
            users = self.__get_items(res)
            users = [user for user in users if user['id'] not in ids]
            for user in users:
                ids.add(user['id'])
            self.__db_driver.write_users_to_db(users)
            print('write to db next users: ', users)
            friends = self.__get_friends(users)
            self.__db_driver.write_friends_to_db(friends)
            print('write to db next friends: ', friends)


    def get_count_users(self):
        res = self.__vk_request('users.search', 'university=1088',main_token)
        return res['response']['count']

