from typing import List

from tenders_recommender.database import Session
from tenders_recommender.model import UsersInteractions


class UsersInteractionsDao(object):

    @staticmethod
    def insert_users_interactions(users_interactions: UsersInteractions) -> None:
        Session.add(users_interactions)
        Session.commit()

    @staticmethod
    def query_all_users_interactions() -> List[UsersInteractions]:
        users_interactions: List[UsersInteractions] = Session.query(UsersInteractions).all()
        return users_interactions
