import json
from datetime import datetime
from typing import List, Optional, Dict, Union

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from recommender_surprise.dto import Recommendation
from recommender_surprise.service import Recommender


print('STARTING RECOMMENDATION SYSTEM')
before: datetime = datetime.now()

app: Flask = Flask(__name__)
CORS(app)
recommender: Recommender = Recommender()

print('READY')
print('TIME ELAPSED: ' + str((datetime.now() - before).total_seconds()))


@app.route('/rmse')
def get_rmse():
    return jsonify(recommender.calculate_rmse())


@app.route('/recommendations/<int:user_id>')
def get_recommendations(user_id: int):
    top: Optional[int] = request.args.get('top', type=int)
    recommendations: List[Recommendation] = recommender.get_recommendations(user_id, top_n=top) \
        if top \
        else recommender.get_recommendations(user_id)

    # json array packed in object so it is safe
    # against redefining js Array constructor exploit
    return jsonify({'data': [r.__dict__ for r in recommendations]})


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


if __name__ == '__main__':
    app.run()
