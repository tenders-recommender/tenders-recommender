import json
from typing import List, Optional, Dict, Union

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from tenders_recommender.dto import Interaction, Recommendation
from tenders_recommender.service import RecommenderService
from tenders_recommender.util import add_descriptions_to_offers

# json arrays are packed in object so it is safe
# against redefining js Array constructor exploit

app: Flask = Flask(__name__)
CORS(app)
recommender_service: RecommenderService = RecommenderService(cache_size=50)


@app.route('/populate_interactions', methods=['POST'])
def populate_interactions():
    interactions: Optional[List[Interaction]] = request.get_json()

    if interactions:
        recommender_service.populate_interactions(interactions)

    return jsonify(True)


@app.route('/train_algorithm')
def train_algorithm():
    recommender_service.train_algorithm()
    return jsonify(True)


@app.route('/rmse')
def get_rmse():
    return jsonify(recommender_service.get_rmse())


@app.route('/recommendations/<int:user_id>')
def get_recommendations(user_id: int):
    top: Optional[int] = request.args.get('top', type=int)
    recommendations: List[Recommendation] = recommender_service.get_recommendations(user_id, top_n=top) \
        if top \
        else recommender_service.get_recommendations(user_id)
    recommendations = add_descriptions_to_offers(recommendations)
    return jsonify({'data': [r._asdict() for r in recommendations]})


@app.route('/rmse/summary')
def get_rmse_summary():
    with open('./rmse_summary.json', 'r') as f:
        data: Dict[str, Union[str, int, float]] = json.load(f)
    return jsonify({'data': data})


@app.route('/alg/comparison')
def get_alg_comparison():
    with open('plots/data/rmse_alg.json', 'r') as f:
        data: Dict[str, Union[str, int, float]] = json.load(f)
    return jsonify({'data': data})


@app.route('/param/comparison')
def get_param_comparison():
    with open('plots/data/rmse_knn_params.json', 'r') as f:
        t = Dict[str, Union[str, int, bool]]
        data: Dict[str, Union[str, int, float, t]] = json.load(f)
    return jsonify({'data': data})


if __name__ == '__main__':
    print('Started Tenders Recommender API')
    app.run()
