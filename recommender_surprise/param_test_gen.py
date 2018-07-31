from surprise import KNNBasic

from recommender_surprise.recommender import Recommender


def main():
    k_range = [1, 10, 20, 45]
    min_k_range = [1, 2, 3]
    name_range = ['cosine', 'msd', 'pearson', 'pearson_baseline']
    min_support_range = [1, 2, 3]

    for k in k_range:
        for min_k in min_k_range:
            for name in name_range:
                for min_support in min_support_range:
                    sim_options = {'name': name,
                                   'min_support': min_support,
                                   'user_based': True
                                   }
                    params = {'k': k, 'min_k': min_k, 'sim_options': sim_options}
                    knn = KNNBasic(k=k, min_k=min_k, sim_options=sim_options)
                    Recommender(algorithm=knn,
                                alg_name=KNNBasic.__name__,
                                rmse_file_name='param_comparison_gen.json',
                                params=params,
                                parsed_data_file_name='parsed_data.bin'
                                )


if __name__ == '__main__':
    main()
