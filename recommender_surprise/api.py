from recommender_surprise.recommender import Recommender
from flask import Flask
from flask import jsonify
from flask import request

print('STARTING RECOMMENDATION SYSTEM')
app = Flask(__name__)
recommender = Recommender(create_inited=True)
print('READY')


@app.route('/rmse')
def get_rmse():
    return jsonify(recommender.calculate_rmse(verbose=False))


@app.route('/recommendations/<int:user_id>')
def get_recommendations(user_id):
    top = request.args.get('top', type=int)
    recommendations = recommender.get_recommendations(user_id, top_n=top) if top \
        else recommender.get_recommendations(user_id)

    # json array packed in object so it is safe
    # against redefining js Array constructor exploit
    return jsonify({'data': recommendations})


if __name__ == '__main__':
    app.run()
