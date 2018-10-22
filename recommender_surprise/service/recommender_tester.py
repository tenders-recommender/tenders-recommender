import json
import os
from itertools import chain
from typing import Tuple, List

from recommender_surprise.dto import Interaction


class RecommenderTester(object):
    __TRACKER_FILE_FOLDER: str = os.path.join('..', '..', 'tracker')
    __INTERACTIONS_FILE_NAMES: List[str] = [
        'observed-offers.json',
        'reported-offers.json',
        'viewed-offers.json'
    ]

    def __init__(self):
        file_paths: Tuple[str, ...] = tuple(os.path.join(self.__TRACKER_FILE_FOLDER, file_name) for file_name in
                                            self.__INTERACTIONS_FILE_NAMES)
        all_interactions: List[Interaction] = list(chain.from_iterable(
            [json.load(open(file_path)) for file_path in file_paths]))
