export class Recommendation {
  private readonly _offer: string;
  private readonly _estimation: number;

  constructor({'offer': offer, 'estimation': estimation}) {
    this._offer = offer;
    this._estimation = estimation;
  }

  get offer(): string {
    return this._offer;
  }

  get estimation(): number {
    return this._estimation;
  }
}
