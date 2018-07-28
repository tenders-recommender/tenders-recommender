export class Algorithm {

  private readonly _algorithm: string;
  private readonly _rmse: number[];
  private readonly _time_elapsed: number[];

  constructor(algorithm: string, rmse: number[], time_elapsed: number[]){
    this._algorithm = algorithm;
    this._rmse = rmse;
    this._time_elapsed = time_elapsed;
  }

  get algorithm(): string {
    return this._algorithm;
  }

  get rsme(): number[] {
    return this._rmse;
  }

  get time_elapsed(): number[] {
    return this._time_elapsed;
  }

  getAverageRmse(): number {
    return this._rmse.reduce(function(acc, val) { return acc + val; }, 0) / this._rmse.length;
  }

  getAverageTimeElapsed(): number {
    return this.time_elapsed.reduce(function(acc, val) { return acc + val; }, 0) / this._time_elapsed.length;
  }

}

