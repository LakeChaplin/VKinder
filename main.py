import random
from random import randrange
import datetime
from time import sleep
import requests
import vk_api
from vk_api.longpoll import VkLongPoll
import database

from system import main_token, user_token, time

vk_session = vk_api.VkApi(token=main_token)
vk = vk_session.get_api()


class VkinderBot:
    # initializing the bot
    def __init__(self):
        print("Let's date!")
        self.vk = vk_api.VkApi(token=main_token)
        self.longpoll = VkLongPoll(self.vk)

    # sending messages to the user on behalf of the community method
    def write_msg(self, user_id, message):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'random_id': randrange(10 ** 7)

                                         }
                       )

    # getting the user-name method
    def get_user_name(self, user_id):
        try:
            first_name = None
            url = f'https://api.vk.com/method/users.get'
            params = {'access_token': user_token,
                      'user_ids': user_id,
                      'v': '5.131'
                      }
            rep = requests.get(url, params=params)
            response = rep.json()
            for items in response['response']:
                for key, value in items.items():
                    first_name = items.get('first_name')
            return first_name
        except Exception as _ex:
            print(f'[INFO] something went wrong: {_ex}')

    # obtaining the gender of the user's pair method
    def reverse_user_gender(self, user_id):
        try:
            searchable_gender = None
            url = 'https://api.vk.com/method/users.get'
            params = {'access_token': user_token,
                      'user_ids': user_id,
                      'v': '5.131',
                      'fields': 'sex'
                      }
            rep = requests.get(url, params=params)
            response = rep.json()
            for items in response['response']:
                for key, value in items.items():
                    gender = items.get('sex')
                    if gender == 1:
                        searchable_gender = 2
                        return searchable_gender
                    elif gender == 2:
                        searchable_gender = 1
                        return searchable_gender
        except Exception as _ex:
            print(f'[INFO] something went wrong: {_ex}')

    # getting the user's city method
    def get_user_city(self, user_id):
        try:
            city = None
            url = 'https://api.vk.com/method/users.get'
            params = {'access_token': user_token,
                      'user_ids': user_id,
                      'v': '5.131',
                      'fields': 'city'
                      }
            rep = requests.get(url, params=params)
            response = rep.json()
            for items in response['response']:
                for key, value in items.items():
                    intermediate = items.get('city')
                    city = intermediate.get('title')
                return city
        except Exception as _ex:
            print(f'[INFO] something went wrong: {_ex}')

    # obtaining the user's city ID method
    def get_user_city_id(self, user_id):
        try:
            global city_id
            url = 'https://api.vk.com/method/users.get'
            params = {'access_token': user_token,
                      'user_ids': user_id,
                      'v': '5.131',
                      'fields': 'city'
                      }
            rep = requests.get(url, params=params)
            response = rep.json()
            for items in response['response']:
                for key, value in items.items():
                    intermediate = items.get('city')
                    city_id = intermediate.get('id')
                return city_id
        except Exception as _ex:
            print(f'[INFO] something went wrong: {_ex}')

    # obtaining the user's age method
    def get_user_age(self, user_id):
        try:
            bdate = None
            url = 'https://api.vk.com/method/users.get'
            params = {'access_token': user_token,
                      'user_ids': user_id,
                      'v': '5.131',
                      'fields': 'bdate'
                      }
            rep = requests.get(url, params=params)
            response = rep.json()

            sleep(time)
            for items in response['response']:
                sleep(time)
                for key, value in items.items():
                    bdate = items.get('bdate')
                return bdate
        except Exception as _ex:
            print(f'[INFO] something went wrong: {_ex}')

    # determining the minimum age of a user's pair method
    def min_age_difference(self, user_id):
        try:
            user_age = self.get_user_age(user_id)
            user_bdate = user_age.split('.')
            if len(user_bdate) == 3:
                user_bday_year = int(user_bdate[2])
                current_year = datetime.date.today().year
                age = current_year - user_bday_year - 3
                return age
        except Exception as _ex:
            print(f'[INFO] something went wrong: {_ex}')

    # determining the maximum age of a user's pair method
    def max_age_difference(self, user_id):
        try:
            user_age = self.get_user_age(user_id)
            user_bdate = user_age.split('.')
            if len(user_bdate) == 3:
                user_bday_year = int(user_bdate[2])
                current_year = datetime.date.today().year
                age = current_year - user_bday_year + 3
                return age
        except Exception as _ex:
            print(f'[INFO] something went wrong: {_ex}')

    # the method of finding a pair for the user
    def pair_search(self, user_id):
        try:
            people_list = []
            offset = 0
            url = f'https://api.vk.com/method/users.search'
            params = {'access_token': user_token,
                      'v': '5.131',
                      'fields': 'first_name, last_name, is_closet, id',
                      'status': '1' or '6',
                      'count': 30,
                      'sex': self.reverse_user_gender(user_id),
                      'city': self.get_user_city_id(user_id),
                      'age_from': self.min_age_difference(user_id),
                      'has_photo': 1,
                      'age_to': self.max_age_difference(user_id)

                      }
            rep = requests.get(url, params=params)
            response = rep.json()
            offset += 10
            items = response['response']['items']
            profile_url = 'https://vk.com/id'
            for persons in items:
                if persons.get('is_closed') == False:
                    person = [
                        persons['id'], persons['first_name'], persons['last_name'],
                        profile_url + str(persons['id'])
                    ]
                    people_list.append(person)
                    database.insert_data_into_users_table(persons['id'], persons['first_name'], persons['last_name'],
                                                          profile_url + str(persons['id']))

            return people_list
        except Exception as _ex:
            print(f'[INFO] something went wrong: {_ex}')



    # method for getting the top 3 photos of a user's couple
    def get_top_photo(self, user_id):
        try:
            url = f'https://api.vk.com/method/photos.get'
            params = {'access_token': user_token,
                      'owner_id': database.unseen_profile()[0],
                      'album_id': 'profile',
                      'extended': 1,
                      'photo_sizes': 1,
                      'is_closed': False,
                      'v': '5.131',
                      'count': 3
                      }

            response = requests.get(url, params=params).json()

            photos_list = []
            for i in range(3):
                try:
                    photos_list.append(([
                        response['response']['items'][i]['likes']['count'],
                        'photo' +
                        str(response['response']['items'][i]['owner_id']) + '_' +
                        str(response['response']['items'][i]['id'])
                    ]))
                except IndexError:
                    photos_list.append(['нет фото'])

            return photos_list
        except Exception as _ex:
            print(f'[INFO] something went wrong: {_ex}')

    def get_id_viewed_user(self, user_id):
        try:
            id = None
            for i in self.get_top_photo(user_id):
                s = (i[1]).split('photo')
                q = s[1].split('_')
                id = q[0]
            database.insert_data_into_viewed_users_table(id)
        except Exception as _ex:
            print(f'[INFO] something went wrong: {_ex}')

    # method of sending a photo to the user
    def send_partner(self, user_id):
        try:
            for photo in self.get_top_photo(user_id):
                print(photo)
                self.vk.method('messages.send',
                               {'user_id': user_id,
                                'attachment': f'{photo[1]}',
                                'random_id': randrange(10 ** 7)
                                })
            self.get_id_viewed_user(user_id)
        except Exception as _ex:
            print(f'[INFO] something went wrong: {_ex}')

    # method of layout of information about the found user-page
    def found_person_info(self):
        try:
            tuple_person = database.unseen_profile()
            list_person = []
            for i in tuple_person:
                list_person.append(i)
            return f'{list_person[1]} {list_person[2]}, ссылка - {list_person[3]}'
        except Exception as _ex:
            print(f'[INFO] something went wrong: {_ex}')


vkinder = VkinderBot()
