export class Simoptions {
  private readonly _name: string;
  private readonly _min_support: number;
  private readonly _user_based: boolean;


  constructor({'name': name, 'min_support': min_support, 'user_based': user_based}) {
    this._name = name;
    this._min_support = min_support;
    this._user_based = user_based;
  }

  get name(): string {
    return this._name;
  }

  get min_support(): number {
    return this._min_support;
  }

  get user_based(): boolean {
    return this._user_based;
  }


}
