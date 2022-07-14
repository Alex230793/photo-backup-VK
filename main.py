import requests
import datetime
import json
from tqdm import tqdm




def max_size_photo(dict_photo):
    """оставялем ссылки на самые большие фото"""
    max_dpi = 0
    need_elem = 0
    for j in range(len(dict_photo)):
        file_dpi = dict_photo[j].get('width') * dict_photo[j].get('height')
        if file_dpi > max_dpi:
            max_dpi = file_dpi
            need_elem = j
    return dict_photo[need_elem].get('url'), dict_photo[need_elem].get('type')

def time_convert(time_unix):
    """преобразование даты"""
    time_bc = datetime.datetime.fromtimestamp(time_unix)
    str_time = time_bc.strftime('%Y-%m-%d time %H-%M-%S')
    return str_time

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



class Yandex:

    def __init__(self, folder_name, token_list, numb=5):
        self.token = token_list
        self.added_files_numb = numb
        self.url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self.headers = {'Authorization': self.token}
        self.folder = self.creating_folder(folder_name)

    def creating_folder(self, folder_name):
        """создаем папку на я-диске"""
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        if requests.get(url, headers=self.headers, params=params).status_code != 200:
            requests.put(url, headers=self.headers, params=params)
            print(f'Создана папка с именем {folder_name}\n')
        else:
            print(f'Такое имя уже существует - {folder_name} \n')
        return folder_name

    def download_link_folder(self, folder_name):
        """ссылка для загрузки я-диск"""
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': folder_name}
        # resource = requests.patch(url, headers=self.headers, params=params).json()['_embedded']['items']
        resource = requests.get(url, headers=self.headers, params=params).json()['_embedded']['items']
        list_to_download = []
        for elem in resource:
            list_to_download.append(elem['name'])
        return list_to_download

    def uploading_folder(self, dict_files):
        """загрузка на я-диск"""
        files_in_folder = self.download_link_folder(self.folder)
        number_downloads = 0
        for key, value in zip(dict_files.keys(), tqdm(range(self.added_files_numb))):
            if number_downloads < self.added_files_numb:
                if key not in files_in_folder:
                    params = {'path': f'{self.folder}/{key}',
                              'url': dict_files[key],
                              'overwrite': 'false'}
                    requests.post(self.url, headers=self.headers, params=params)
                    number_downloads += 1
                else:
                    print(f' Такой файл {key} уже существует')
            else:
                break

        print(f'Загруженно {number_downloads} файлов')


token_ya = ''
access_token = ''
user_id = ''

vk = VK(access_token, user_id)

with open('vk_photo.json', 'w') as file:  # Сохранение  списка в файл
    json.dump(vk.json, file)


ya_disk = Yandex('vk_photo', token_ya)
ya_disk.uploading_folder(vk.dict_unloading)


