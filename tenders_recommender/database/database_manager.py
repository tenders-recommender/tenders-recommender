from tenders_recommender.dao.user_interactions import UsersInteractions
from tenders_recommender.database.base import engine, Base, Session


class DatabaseManager:

    def __init__(self):
        Base.metadata.create_all(engine)

    def insert_users_interactions(self, users_interactions):
        session = Session()
        session.add(users_interactions)
        session.commit()
        session.close()

    def query_all_user_interactions(self):
        session = Session()
        users_interactions = session.query(UsersInteractions).all()
        session.close()
        return users_interactions
