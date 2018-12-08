class ResultTypes:
    types = {
        "algorithm_comparison": "ALG_COMPARISON",
        "knn": "KNN_COMPARISON",
        "knn_timesteps": "KNN_TIMESTEPS",
        "svd": "SVD_COMPARISON",
        "svd_timesteps": "SVD_TIMESTEPS",
        "rmse_summary": "RMSE_SUMMARY"
    }

    def getType(self, type: str):
        return self.types[type]
