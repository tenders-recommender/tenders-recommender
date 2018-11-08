export interface SvdParametersComparisonData {
  readonly split0_test_rmse: ReadonlyArray<number>;
  readonly split1_test_rmse: ReadonlyArray<number>;
  readonly split2_test_rmse: ReadonlyArray<number>;
  readonly split3_test_rmse: ReadonlyArray<number>;
  readonly split4_test_rmse: ReadonlyArray<number>;

  readonly mean_test_rmse: ReadonlyArray<number>;
  readonly std_test_rmse: ReadonlyArray<number>;
  readonly rank_test_rmse: ReadonlyArray<number>;

  readonly mean_fit_time: ReadonlyArray<number>;
  readonly std_fit_time: ReadonlyArray<number>;
  readonly mean_test_time: ReadonlyArray<number>;
  readonly std_test_time: ReadonlyArray<number>;

  readonly params: ReadonlyArray<SvdParameters>;
  readonly param_n_factors: ReadonlyArray<number>;
  readonly param_n_epochs: ReadonlyArray<number>;
  readonly param_biased: ReadonlyArray<boolean>;
  readonly param_init_mean: ReadonlyArray<number>;
  readonly param_init_std_dev: ReadonlyArray<number>;
  readonly param_lr_all: ReadonlyArray<number>;
  readonly param_reg_all: ReadonlyArray<number>;
}

export interface SvdParameters {
  readonly n_factors: number;
  readonly n_epochs: number;
  readonly biased: boolean;
  readonly init_mean: number;
  readonly init_std_dev: number;
  readonly lr_all: number;
  readonly reg_all: number;
}
