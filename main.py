import json
from main_def import file_open_read
from Vk_class import VK
from Ya_class import Yandex


access_token = file_open_read('Vk_token')
user_id = file_open_read('user_id')
token_ya = file_open_read('Ya_token')


vk = VK(access_token, user_id)

with open('vk_photo.json', 'w') as file:  # Сохранение  списка в файл
    json.dump(vk.json, file)

ya_disk = Yandex('vk_photo', token_ya)
ya_disk.uploading_folder(vk.dict_unloading)
