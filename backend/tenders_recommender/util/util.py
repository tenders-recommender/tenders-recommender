import os

import pickle


def save_to_file(object_to_save: object, file_path: str) -> None:
    dir_name: str = os.path.dirname(file_path)

    if dir_name is not None and dir_name != '':
        os.makedirs(dir_name, exist_ok=True)

    with open(file_path, 'wb') as result_file:
        pickle.dump(object_to_save, result_file, protocol=pickle.HIGHEST_PROTOCOL)


def load_from_file(file_path: str) -> object:
    with open(file_path, 'rb') as result_file:
        loaded_object = pickle.load(result_file)

    return loaded_object
