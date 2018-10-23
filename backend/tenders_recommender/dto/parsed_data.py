from typing import NamedTuple, Dict

from surprise import Trainset

from .types import Testset


class ParsedData(NamedTuple):
    ids_offers_map: Dict[int, str]
    train_set: Trainset
    test_set: Testset
