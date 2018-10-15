export class RMSE {
  private readonly _rmse: number;
  private readonly _timestamp: number;

  constructor({'timestamp': timestamp, 'rmse': rmse}) {
    this._timestamp = timestamp;
    this._rmse = rmse;
  }

  get timestamp(): number {
    return this._timestamp;
  }

  get rmse(): number {
    return this._rmse;
  }
}
