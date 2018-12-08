class ResultTypes:
    types = {
        "algorithm_comparison": "ALG_COMPARISON",
        "knn": "KNN_COMPARISON",
        "knn_timesteps": "KNN_TIMESTEPS",
        "knn_baseline_als": "KNN_BASELINE_ALS",
        "knn_baseline_als_timesteps": "KNN_BASELINE_TIMESTEPS_ALS",
        "knn_baseline_sgd": "KNN_BASELINE_SGD",
        "knn_baseline_timesteps_sgd": "KNN_BASELINE_TIMESTEPS_SGD",
        "svd": "SVD_COMPARISON",
        "svd_timesteps": "SVD_TIMESTEPS",
        "rmse_summary": "RMSE_SUMMARY"
    }

    def getType(self, type: str):
        return self.types[type]
