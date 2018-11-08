import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ApiArrayData } from '../model/api-array-data';
import { Interaction } from '../model/interaction';
import { AlgorithmsComparisonData } from '../model/plots/algorithms-comparison-data';
import { KnnParametersComparisonData } from '../model/plots/knn-parameters-comparison-data';
import { SvdParametersComparisonData } from '../model/plots/svd-parameters-comparison-data';
import { TimeStepData } from '../model/plots/time-step-data';
import { Recommendation } from '../model/recommendation';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly recommenderServiceUrl = 'http://localhost:5000/';
  private readonly recommendationsUrl = this.recommenderServiceUrl + 'recommendations/';
  private readonly currentDataRmseUrl = this.recommenderServiceUrl + 'rmse/';
  private readonly populateInteractionsUrl = this.recommenderServiceUrl + 'populate_interactions/';
  private readonly trainAlgorithmUrl = this.recommenderServiceUrl + 'train_algorithm/';

  private readonly plotsDataRepositoryUrl = 'https://raw.githubusercontent.com/tenders-recommender/tenders-recommender/master/plots/data/';
  private readonly algorithmsComparisonDataUrl = this.plotsDataRepositoryUrl + 'rmse_alg.json';

  private readonly knnParametersComparisonDataUrl = this.plotsDataRepositoryUrl + 'rmse_knn_params.json';
  private readonly knnTimeStepDataUrl = this.plotsDataRepositoryUrl + 'rmse_knn_time_step.json';
  private readonly svdParametersComparisonDataUrl = this.plotsDataRepositoryUrl + 'rmse_svd_params.json';
  private readonly svdTimeStepDataUrl = this.plotsDataRepositoryUrl + 'rmse_svd_time_step.json';

  constructor(private http: HttpClient) {
  }

  public populateInteractions(interactions: ReadonlyArray<Interaction>): Promise<boolean> {
    return this.http.post(this.populateInteractionsUrl, interactions)
      .toPromise()
      .then(() => true, () => false);
  }

  public trainAlgorithm(): Promise<boolean> {
    return this.http.get(this.trainAlgorithmUrl)
      .toPromise()
      .then(() => true, () => false);
  }

  public getRecommendations(userId: number, topN?: number): Promise<ReadonlyArray<Recommendation>> {
    let requestOptions = {};

    if (topN) {
      requestOptions = {
        params: { top: topN }
      };
    }

    return this.http.get<ApiArrayData<Recommendation>>(this.recommendationsUrl + userId, requestOptions)
      .toPromise()
      .then(apiData => apiData.data);
  }

  public getCurrentRmse(): Promise<number> {
    return this.http.get<number>(this.currentDataRmseUrl)
      .toPromise();
  }

  public getAlgorithmsComparisonData(): Promise<ReadonlyArray<AlgorithmsComparisonData>> {
    return this.http.get<ReadonlyArray<AlgorithmsComparisonData>>(this.algorithmsComparisonDataUrl)
      .toPromise();
  }

  public getKnnParametersComparisonData(): Promise<ReadonlyArray<KnnParametersComparisonData>> {
    return this.http.get<ReadonlyArray<KnnParametersComparisonData>>(this.knnParametersComparisonDataUrl)
      .toPromise();
  }

  public getKnnTimeStepData(): Promise<ReadonlyArray<TimeStepData>> {
    return this.http.get<ReadonlyArray<TimeStepData>>(this.knnTimeStepDataUrl)
      .toPromise();
  }

  public getSvdParametersComparisonData(): Promise<SvdParametersComparisonData> {
    return this.http.get<SvdParametersComparisonData>(this.svdParametersComparisonDataUrl)
      .toPromise();
  }

  public getSvdTimeStepData(): Promise<ReadonlyArray<TimeStepData>> {
    return this.http.get<ReadonlyArray<TimeStepData>>(this.svdTimeStepDataUrl)
      .toPromise();
  }
}
