export interface PartialAlgorithmsComparisonData {
  readonly rmse: number;
  readonly time_elapsed: number;
}

export interface AlgorithmsComparisonData extends PartialAlgorithmsComparisonData {
  readonly algorithm: string;
}
