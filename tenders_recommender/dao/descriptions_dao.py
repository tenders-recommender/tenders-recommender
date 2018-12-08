from typing import List

from tenders_recommender.database import Session
from tenders_recommender.model import Descriptions


class DescriptionsDao(object):

    @staticmethod
    def insert_description(descriptions: Descriptions) -> None:
        Session.add(descriptions)
        Session.commit()

    @staticmethod
    def query_all_descriptions() -> List[Descriptions]:
        json = Session.query(Descriptions).all()
        return json
