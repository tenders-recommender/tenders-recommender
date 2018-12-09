from tenders_recommender.parser import Parser


class TestParser(object):

    def test_parse(self):
        # given
        interactions_list = [
            {
                "type": "reported-offer",
                "who": 159,
                "what": "bzp-2017-n-533981",
                "when": "2017-06-16T16:09:43.674+02:00",
                "score": 2.5599573
            },
            {
                "type": "observed-offer",
                "who": 141,
                "what": "bzp-2017-n-533982",
                "when": "2017-06-15T16:09:43.674+02:00"
            }
        ]
        score_map = {
            'observed-offer': 5.0,
            'reported-offer': 3.0,
            'viewed-offer': 4.0
        }
        rating_scale = (1, 5)

        parser = Parser()

        # when
        parsed_data = parser.parse(interactions_list, score_map=score_map, rating_scale=rating_scale)

        # then
        assert parsed_data.ids_offers_map == {1: 'bzp-2017-n-533981', 2: 'bzp-2017-n-533982'}
        assert parsed_data.whole_data_set.df.to_dict() == {
            'user_id': {0: 159, 1: 141},
            'offer_id': {0: 1, 1: 2},
            'score': {0: 3.0, 1: 5.0}
        }
        assert parsed_data.test_set == [(159, 2, 4.0), (141, 1, 4.0)]
        assert parsed_data.train_set is not None
