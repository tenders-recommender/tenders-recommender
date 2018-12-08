from typing import List, Optional

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from tenders_recommender.database import Session, init_database
from tenders_recommender.model import Interaction, Recommendation, TestResults, ResultTypes
from tenders_recommender.service import RecommenderService
from tenders_recommender.util import add_descriptions_to_offers
from tenders_recommender.dao import TestResultsDao

# json arrays are packed in object so it is safe
# against redefining js Array constructor exploit

service_api: Flask = Flask(__name__)
CORS(service_api)
recommender_service: RecommenderService = RecommenderService(cache_size=50)


@service_api.route('/populate_interactions', methods=['POST'])
def populate_interactions():
    interactions: Optional[List[Interaction]] = request.get_json()

    if interactions:
        recommender_service.populate_interactions(interactions)

    return jsonify('Populated interactions correctly')


@service_api.route('/train_algorithm')
def train_algorithm():
    try:
        recommender_service.train_algorithm()
        return jsonify('Algorithm trained correctly')
    except ValueError as e:
        return jsonify(e)


@service_api.route('/rmse')
def get_rmse():
    return jsonify(recommender_service.get_rmse())


@service_api.route('/recommendations/<int:user_id>')
def get_recommendations(user_id: int):
    top: Optional[int] = request.args.get('top', type=int)
    recommendations: List[Recommendation] = recommender_service.get_recommendations(user_id, top_n=top) \
        if top \
        else recommender_service.get_recommendations(user_id)
    recommendations = add_descriptions_to_offers(recommendations)
    return jsonify({'data': [r._asdict() for r in recommendations]})


@service_api.route('/results/<string:type>')
def get_param_comparison(type: str):
    data = TestResultsDao().query_results(type)
    return data


@service_api.teardown_appcontext
def remove_database_session(exc=None):
    Session.close()


def start_service():
    init_database()
    service_api.run()
    print('Started Tenders Recommender API')
