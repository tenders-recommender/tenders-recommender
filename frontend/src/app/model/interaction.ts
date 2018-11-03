export interface Interaction {
  readonly type: string;
  readonly who: number;
  readonly what: string;
  readonly when: string;
  readonly score?: number;
}
