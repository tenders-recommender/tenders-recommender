import { Route } from '@angular/router';

export interface NavLink extends Route {
  readonly label: string;
}
