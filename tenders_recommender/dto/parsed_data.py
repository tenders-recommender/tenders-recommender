from typing import NamedTuple, Dict

from surprise import Trainset
from surprise.dataset import DatasetAutoFolds

from .types import Testset


class ParsedData(NamedTuple):
    ids_offers_map: Dict[int, str]
    whole_data_set: DatasetAutoFolds
    train_set: Trainset
    test_set: Testset
