from typing import List, Tuple, Union, NamedTuple

from bidict import bidict
from numpy.core.multiarray import ndarray
from pandas import DataFrame
from surprise import Trainset


class ParsedData(NamedTuple):
    offers_id_bi_map: bidict
    train_set: Trainset = None
    test_set: List[Tuple[str, str, Union[ndarray, float]]] = None
    data_frame: DataFrame = None
