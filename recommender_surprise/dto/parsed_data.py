from typing import List, Tuple, Union

from bidict import bidict
from numpy.core.multiarray import ndarray
from pandas import DataFrame
from surprise import Trainset


class ParsedData(object):
    def __init__(self,
                 offers_id_bi_map: bidict,
                 train_set: Trainset = None,
                 test_set: List[Tuple[str, str, Union[ndarray, float]]] = None,
                 data_frame: DataFrame = None):
        self.offers_id_bi_map: bidict = offers_id_bi_map
        self.train_set = train_set
        self.test_set = test_set
        self.data_frame = data_frame
