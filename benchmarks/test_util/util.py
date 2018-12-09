import json
import os
from datetime import datetime
from itertools import chain
from typing import Tuple, List, Dict, Callable

import dateutil.parser
import numpy as np

from tenders_recommender.dao import TestResultsDao
from tenders_recommender.database import init_database, Session
from tenders_recommender.model.result_types import ResultTypes
from tenders_recommender.model.test_results import TestResults
from tenders_recommender.dto import Interaction

SAVED_FOLDER: str = os.path.join('..', '..', 'plots', 'data')
RESOURCES_FILE_FOLDER: str = os.path.join('..', '..', 'resources')
INTERACTIONS_FILE_NAMES: List[str] = [
    'observed-offers.json',
    'reported-offers.json',
    'viewed-offers.json'
]


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()

        return json.JSONEncoder.default(self, obj)


def load_sorted_test_interactions() -> List[Interaction]:
    file_paths: Tuple[str, ...] = tuple(os.path.join(RESOURCES_FILE_FOLDER, file_name)
                                        for file_name in INTERACTIONS_FILE_NAMES)

    interaction_date_getter: Callable[[Interaction], datetime] = lambda interaction: \
        dateutil.parser.parse(interaction['when'])

    interactions: List[Interaction] = sorted(chain.from_iterable(
        [json.load(open(file_path)) for file_path in file_paths]), key=interaction_date_getter)

    return interactions


def add_rmse_to_file(rmse: float,
                     file_name: str,
                     *additional_params: Tuple[str, object]) -> None:
    file_path: str = create_file_path(file_name)

    entry: Dict[str, object] = {'rmse': rmse}

    for param_tuple in additional_params:
        entry[param_tuple[0]] = param_tuple[1]

    entries = []
    if os.path.isfile(file_path):
        with open(file_path, 'r') as rmse_file:
            entries: list = json.load(rmse_file)

    entries.append(entry)

    with open(file_path, 'w') as rmse_file:
        json.dump(entries, rmse_file)


def add_results_to_database(results, type, cls=None) -> None:
    init_database()
    res = TestResults(ResultTypes.types[type], json.dumps(results, cls=cls))
    testResultsDao = TestResultsDao()
    testResultsDao.insert_results(res)
    Session.close()


def create_file_path(file_name: str) -> str:
    return os.path.join(SAVED_FOLDER, file_name) \
        if file_name is not None \
        else None
