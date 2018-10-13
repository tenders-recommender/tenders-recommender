from typing import NamedTuple

from bidict import bidict
from pandas import DataFrame
from surprise import Trainset

from recommender_surprise.dto.types import Testset


class ParsedData(NamedTuple):
    offers_id_bi_map: bidict
    train_set: Trainset = None
    test_set: Testset = None
    data_frame: DataFrame = None
