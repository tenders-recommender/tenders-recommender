from bidict import bidict


class ParsedData(object):
    def __init__(self, offers_id_bi_map: bidict, train_set, test_set):
        self.offers_id_bi_map: bidict = offers_id_bi_map
        self.train_set = train_set
        self.test_set = test_set
