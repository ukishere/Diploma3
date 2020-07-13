import requests
import time
import settings
from urllib.parse import urlencode
from datetime import datetime
from pymongo import MongoClient


class User:
    def __init__(self):
        print('Добро пожаловать во VKinder!')
        self.user_id = input('Введите id пользователя: ')
        print('?'.join((settings.oauth_vk_url, urlencode(settings.init_parameters))))
        self.user_token = input('Пройдите по ссылке и введите полученный токен: ')

        # Тестовые значения
        self.user_id = 594982409
        self.user_token = '58a805b8f8a9d44cc9cb4a7f3099b74cb48cb89ce5a4f29d1d3928b6534f74d2c079a9d7dee089306926a'

    def get_response(self, api_method, params):
        response = requests.get(settings.api_vk_url+api_method, params)
        try:
            if response.json()['error']['error_code'] == 5:
                print('Ошибка авторизации.')
                exit()
            elif response.json()['error']['error_code'] == 6:
                time.sleep(3)
                response = requests.get(settings.api_vk_url + api_method, params)
                return response.json()
            elif response.json()['error']['error_code'] == 30:
                return None
        except KeyError:
            return response.json()

    def check_user(self):
        settings.check_user_parameters['user_ids'] = self.user_id

        response = self.get_response(settings.check_user_method, settings.check_user_parameters)
        try:
            if response['error']['error_code'] == 113:
                print('Неверно указан идентификатор пользователя.')
                exit()
            elif response['error']['error_code'] == 5:
                print('Неверно указан токен пользователя.')
                exit()
        except KeyError:
            self.user_id = int(response['response'][0]['id'])

        try:
            self.city = response['response'][0]['city']['id']
        except KeyError:
            self.city = input('Пожалуйста введите ваш город: ')

        try:
            self.sex = response['response'][0]['sex']
        except KeyError:
            self.sex = input('Пожалуйста введите ваш пол: ')

        try:
            self.bdate = response['response'][0]['bdate']
        except KeyError:
            self.bdate = input(f'Пожалуйста введите дату вашего рождения: ')

        try:
            self.relation = response['response'][0]['relation']
        except KeyError:
            self.relation = input(f'Пожалуйста введите ваше семейное положение: ')

        self.year = self.bdate.split('.')
        try:
            self.year = int(self.year[2])
        except IndexError:
            print('Для работы программы необходимо указать год рождения')
            exit()

        self.age = int(datetime.now().year) - self.year
        if self.age < 18:
            print('18+. Только для взрослых. Расскажи родителям.')
            exit()

    def get_victims(self, offset):
        if self.sex == 1:
            settings.get_victims_parameters['sex'] = 2
        elif self.sex == 2:
            settings.get_victims_parameters['sex'] = 1

        settings.get_victims_parameters['city'] = self.city
        settings.get_victims_parameters['relation'] = self.relation
        settings.get_victims_parameters['access_token'] = self.user_token
        settings.get_victims_parameters['age_to'] = self.age + 5
        settings.get_victims_parameters['age_from'] = self.age - 5
        settings.get_victims_parameters['offset'] = offset

        victims = []
        response = self.get_response(settings.get_victims_method, settings.get_victims_parameters)

        for victim in response['response']['items']:
            try:
                birth_year = int(victim['bdate'].split('.')[2])
                if birth_year == None:
                    continue
                elif birth_year < self.year - 5 or birth_year > self.year + 5 or (int(datetime.now().year) - birth_year) < 18:
                    continue
            except KeyError:
                continue
            except IndexError:
                continue
            if victim['is_friend'] == 0 and victim['blacklisted_by_me'] == 0:
                victims.append(
                    {
                        'Name': victim['first_name'] + ' ' + victim['last_name'],
                        'Vkid': victim['id'],
                        'Page': 'https://vk.com/id' + str(victim['id'])
                    }
                )

        return victims

    def create_database(self):
        client = MongoClient()
        vkinder_database = client['vkinder_database']
        self.users_data = vkinder_database[f'{self.user_id}']

    def check_victims(self, victims):
        new_victims = []
        for victim in victims:
            if not bool(list(self.users_data.find({'Vkid': victim['Vkid']}, {}))):
                new_victims.append(victim)
        return new_victims

    def remember_victims(self, new_victims):
        self.users_data.insert_many(new_victims)

    def add_victims_photo(self, victims):
        for victim in victims:
            settings.add_victims_photo_parameters['owner_id'] = victim['Vkid']
            response = self.get_response(settings.add_victims_photo_method, settings.add_victims_photo_parameters)

            if response == None:
                continue

            photos_list = []
            for photo in response['response']['items']:
                likes_and_comments = photo['likes']['count'] + photo['comments']['count']
                for link in photo['sizes']:
                    if link['type'] == 'x':
                        photos_list.append((likes_and_comments,link['url']))

            photos_list.sort()
            photos_list.reverse()
            victim['Photos'] = {'Top1': '', 'Top2': '','Top3': ''}

            try:
                victim['Photos']['Top1'] = photos_list[0][1]
                victim['Photos']['Top2'] = photos_list[1][1]
                victim['Photos']['Top3'] = photos_list[2][1]
            except IndexError:
                pass