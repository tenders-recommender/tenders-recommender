import os

import pickle
import re

from typing import List, Dict
from collections import ChainMap
from tenders_recommender.dao import DescriptionsDao
from tenders_recommender.model import Recommendation

YEAR_REGEX = re.compile(r'(?:\b|\D)(\d{4})(?:\b|\D)')
ID_REGEX = re.compile(r'(\d+)')


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


def add_descriptions_to_offers(recommendations: List[Recommendation]) -> List[Recommendation]:
    recommendations_with_desc: List[Recommendation] = []

    descriptions_dao = DescriptionsDao()
    results = descriptions_dao.query_all_descriptions()
    descriptions_list: List = []
    for result in results:
        descriptions_list.append(result.data)
    descriptions = dict(ChainMap(*descriptions_list))

    for r in recommendations:
        desc = find_description(descriptions, r.offer)
        recommendations_with_desc.append(Recommendation(r.offer, r.estimation, desc))

    return recommendations_with_desc


def find_description(descriptions: Dict[str, str], offer: str) -> str:
    if 'bzp' not in offer:
        return '-'

    year = YEAR_REGEX.findall(offer)[0]
    offer_without_year = offer.replace(year, '')

    offer_id_list = ID_REGEX.findall(offer_without_year)
    offer_id = offer_id_list[0] if len(offer_id_list) == 1 else offer_id_list[1]

    offer_key = offer_id + '-' + year
    description = descriptions[offer_key]

    if description is not None:
        return description
    else:
        return '-'
