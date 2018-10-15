import {Simoptions} from "./simoptions";

export class Params {

  private readonly _algorithm: string;
  private readonly _rmse: number;
  private readonly _time_elapsed: number;
  private readonly _k: number;
  private readonly _min_k: number;
  private readonly _simoptions: Simoptions;

  constructor({'algorithm': algorithm, 'rmse': rmse, 'time_elapsed': time_elapsed, 'k': k, 'min_k': min_k, 'sim_options': sim_options}) {
    this._algorithm = algorithm;
    this._rmse = rmse;
    this._time_elapsed = time_elapsed;
    this._k = k;
    this._min_k = min_k;
    this._simoptions = new Simoptions(sim_options);
  }

  get algorithm(): string {
    return this._algorithm;
  }

  get rmse(): number {
    return this._rmse;
  }

  get time_elapsed(): number {
    return this._time_elapsed;
  }

  get k(): number {
    return this._k;
  }

  get min_k(): number {
    return this._min_k;
  }

  get simoptions(): Simoptions {
    return this._simoptions;
  }
}
