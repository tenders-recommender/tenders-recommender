from tenders_recommender.util.util import find_description
import unittest


class TestFindDescription(unittest.TestCase):

    def test_should_return_dash_when_none_offer_is_bzp(self):
        # given
        offer_id = "2015_S_208-377616_ted"
        descriptions = {offer_id: "New apartments"}
        # when
        description = find_description(descriptions, offer_id)
        # then
        self.assertEqual(description, "-")

    def test_should_return_dash_when_none_offer_is_found(self):
        # given
        offer_id_key = "534591-2017"
        descriptions = {offer_id_key: "New apartments"}

        non_existing_id = "bzp-2017-n-537449"
        # when
        description = find_description(descriptions, non_existing_id)
        # then
        self.assertEqual(description, "-")

    def test_should_return_description(self):
        # given
        key_id = "534591-2017"
        existing_offer_id = "bzp-2017-n-534591"
        descriptions = {key_id: "New apartments"}

        # when
        description = find_description(descriptions, existing_offer_id)

        # then
        self.assertEqual(description, "New apartments")


if __name__ == '__main__':
    unittest.main()
