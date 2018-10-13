import json
from datetime import datetime

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from recommender_surprise.service import Recommender

print('STARTING RECOMMENDATION SYSTEM')
before = datetime.now()

app = Flask(__name__)
CORS(app)
recommender = Recommender()

after = datetime.now()
print('READY')
print('TIME ELAPSED: ' + str((after - before).total_seconds()))


@app.route('/rmse')
def get_rmse():
    return jsonify(recommender.calculate_rmse())


@app.route('/recommendations/<int:user_id>')
def get_recommendations(user_id):
    top = request.args.get('top', type=int)
    recommendations = recommender.get_recommendations(user_id, top_n=top) \
        if top \
        else recommender.get_recommendations(user_id)

    # json array packed in object so it is safe
    # against redefining js Array constructor exploit
    return jsonify({'data': [r.__dict__ for r in recommendations]})


@app.route('/rmse/summary')
def get_rmse_summary():
    with open('./rmse_summary.json', 'r') as f:
        data = json.load(f)
    return jsonify({'data': data})


@app.route('/alg/comparison')
def get_alg_comparison():
    with open('plots/data/rmse_alg.json', 'r') as f:
        data = json.load(f)
    return jsonify({'data': data})


if __name__ == '__main__':
    app.run()
