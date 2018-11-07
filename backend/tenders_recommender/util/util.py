import json
import os

import pickle
import re

from typing import List

from tenders_recommender.dto import Recommendation

DATA_FILE_FOLDER: str = os.path.join('..', '..', '..', 'plots', 'data')


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


def add_descriptions_to_offers(recommendations: List[Recommendation]):
    file_path = os.path.join(DATA_FILE_FOLDER, 'description.json')
    recommendations_with_desc: List[Recommendation] = []
    with open(file_path) as file:
        descriptions = json.load(file)
    for r in recommendations:
        desc = find_description(descriptions, r.offer)
        recommendations_with_desc.append(Recommendation(r.offer, r.estimation, desc))
    return recommendations_with_desc


def find_description(descriptions: List, offer: str):
    if not offer.__contains__('bzp'):
        return '-'
    for desc in descriptions:
        key = desc.keys().__iter__().__next__()
        value = desc.values().__iter__().__next__()
        id = re.search(r'\d+', key).group().strip()
        year = key.rsplit('-', 1)[1].strip()
        if offer.__contains__(id) and offer.__contains__(year):
            return value

    return '-'
