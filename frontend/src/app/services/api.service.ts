import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AlgorithmsComparisonData } from '../model/plots/algorithms-comparison-data';
import { ApiArrayData } from '../model/api-array-data';
import { Interaction } from '../model/interaction';
import { ParametersComparisonData } from '../model/plots/parameters-comparison-data';
import { Recommendation } from '../model/recommendation';
import { TimeStepData } from '../model/plots/time-step-data';

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
  private readonly parametersComparisonDataUrl = this.plotsDataRepositoryUrl + 'rmse_params.json';
  private readonly timeStepDataUrl = this.plotsDataRepositoryUrl + 'rmse_time_step.json';

  constructor(private http: HttpClient) {
  }

  public populateInteractions(interactions: Array<Interaction>): Promise<boolean> {
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

  public getParametersComparisonData(): Promise<ReadonlyArray<ParametersComparisonData>> {
    return this.http.get<ReadonlyArray<ParametersComparisonData>>(this.parametersComparisonDataUrl)
      .toPromise();
  }

  public getTimeStepData(): Promise<ReadonlyArray<TimeStepData>> {
    return this.http.get<ReadonlyArray<TimeStepData>>(this.timeStepDataUrl)
      .toPromise();
  }
}
