import datetime
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


def file_open_read(file):
    """функция чтения информации из файла"""
    with open(file, 'r') as file_read:
        info = file_read.read()
    return(info)





