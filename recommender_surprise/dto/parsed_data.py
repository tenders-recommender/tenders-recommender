from typing import NamedTuple, Optional

from bidict import bidict
from pandas import DataFrame
from surprise import Trainset

from recommender_surprise.dto.types import Testset


class ParsedData(NamedTuple):
    offers_id_bi_map: bidict
    train_set: Optional[Trainset] = None
    test_set: Optional[Testset] = None
    data_frame: Optional[DataFrame] = None
