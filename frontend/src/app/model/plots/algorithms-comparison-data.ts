export interface AlgorithmsComparisonData extends PartialAlgorithmsComparisonData{
  readonly algorithm: string;
}

export interface PartialAlgorithmsComparisonData {
  readonly rmse: number;
  readonly time_elapsed: number;
}
