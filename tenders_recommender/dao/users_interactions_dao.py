from typing import List

from tenders_recommender.database import Session
from tenders_recommender.model import Interaction, UsersInteractions


class UsersInteractionsDao(object):

    @staticmethod
    def insert_users_interactions(users_interactions) -> None:
        Session.add(users_interactions)
        Session.commit()

    @staticmethod
    def query_all_users_interactions() -> List[Interaction]:
        users_interactions: List[Interaction] = Session.query(UsersInteractions).all()
        return users_interactions
