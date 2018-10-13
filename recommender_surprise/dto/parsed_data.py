from bidict import bidict
from pandas import DataFrame


class ParsedData(object):
    def __init__(self,
                 offers_id_bi_map: bidict,
                 train_set=None,
                 test_set=None,
                 data_frame: DataFrame = None):
        self.offers_id_bi_map: bidict = offers_id_bi_map
        self.train_set = train_set
        self.test_set = test_set
        self.data_frame = data_frame
