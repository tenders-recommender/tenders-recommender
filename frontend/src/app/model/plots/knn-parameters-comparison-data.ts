export interface KnnParametersComparisonData {
  readonly rmse: number;
  readonly algorithm: string;
  readonly time_elapsed: number;
  readonly k: number;
  readonly min_k: number;
  readonly sim_options: SimOptions;
}

export interface SimOptions {
  readonly name: string;
  readonly min_support: number;
  readonly user_based: boolean;
}
