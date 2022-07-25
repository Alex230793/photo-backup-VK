import requests
from tqdm import tqdm


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

