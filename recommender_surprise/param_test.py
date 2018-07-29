import json

from recommender_surprise.parser import Parser
from surprise import KNNBasic, Dataset, Reader, SVD
from surprise.model_selection import GridSearchCV
import pandas as pd
import os.path


def main():
    parser = Parser()
    parser_data = parser.parse(without_train_set=True)
    reader = Reader()
    data = Dataset.load_from_df(parser_data.data_frame, reader)

    print(data)
    print("Data frame loaded")

    param_grid = {'k': [10, 25, 45],
                  'min_k': [1, 2, 3],
                  'sim_options':
                      {
                          'name': ['pearson', 'cosine', 'msd', 'pearson_baseline'],
                          'min_support': [1, 2, 3],
                          'user_based': [False]}
                  }
    gs = GridSearchCV(KNNBasic, param_grid, measures=['rmse'], cv=3)

    gs.fit(data)

    print(gs.best_score['rmse'])
    print(gs.best_params['rmse'])

    add_gs_results_to_file(gs)


def add_gs_results_to_file(gs: GridSearchCV):
    results_df = pd.DataFrame.from_dict(gs.cv_results)
    json_res = results_df.to_json()
    file_path = os.path.join('saved', 'param_comparison.json')
    best_param_file_path = os.path.join('saved', 'best_param.json')
    with open(file_path, 'w') as json_file:
        json_file.write(json_res)
    with open(best_param_file_path, 'w') as best_file:
        json_object = {
            'best_score': gs.best_score['rmse'],
            'best_params': gs.best_params['rmse']
        }
        json.dump(json_object, best_file)


if __name__ == '__main__':
    main()
