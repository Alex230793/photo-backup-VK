import requests
from main_def import max_size_photo, time_convert


class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.json, self.dict_unloading = self.dict_unloading_photo()


    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()


    def users_photo(self):
        """определяем кол-во фотографий и их список"""
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'album_id': 'profile', 'photo_sizes': 1, 'extended': 1, 'rev': 1}
        photo_info = requests.get(url, params={**self.params, **params}).json()['response']
        return photo_info['count'], photo_info['items']


    def sort_users_photo(self):
        """словарь: ключ кол-во лайков, значение - лайки, дата и ссылка для загрузки"""
        count_photo, photo_items = self.users_photo()
        result = {}
        for photo_score in range(count_photo):
            numb_likes = photo_items[photo_score]['likes']['count']
            url_download, picture_size = max_size_photo(photo_items[photo_score]['sizes'])
            time_warp = time_convert(photo_items[photo_score]['date'])
            new_value = result.get(numb_likes, [])
            new_value.append({'likes_count': numb_likes,
                              'add_name': time_warp,
                              'url_picture': url_download,
                              'size': picture_size})
            result[numb_likes] = new_value
        return result


    def dict_unloading_photo(self):
        """получаем словарь и json файл"""
        json_list = []
        sorted_dict = {}
        picture_dict = self.sort_users_photo()
        counter = 0
        for elem in picture_dict.keys():
            for value in picture_dict[elem]:
                if len(picture_dict[elem]) == 1:
                    file_name = f'{value["likes_count"]}.jpeg'
                else:
                    file_name = f'{value["likes_count"]} {value["add_name"]}.jpeg'
                    json_list.append({'file name': file_name, 'size': value["size"]})
                if value["likes_count"] == 0:
                    sorted_dict[file_name] = picture_dict[elem][counter]['url_picture']
                    counter += 1
                else:
                    sorted_dict[file_name] = picture_dict[elem][0]['url_picture']
        return json_list, sorted_dict


