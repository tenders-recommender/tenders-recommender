import { Routes } from '@angular/router';
import { PlotsComponent } from '../components/plots/plots.component';
import { RecommendationsComponent } from '../components/recommendations/recommendations.component';
import { TrainingComponent } from '../components/training/training.component';
import { NavLink } from '../model/routing/nav-link';
import { PLOTS_ROUTES } from './plots-routes';

export const NAV_LINKS: NavLink[] = [
  { path: 'recommendations', component: RecommendationsComponent, label: 'Recommendations' },
  { path: 'training', component: TrainingComponent, label: 'Algorithm Training' },
  { path: 'plots', component: PlotsComponent, label: 'Plots', children: PLOTS_ROUTES }
];

export const ROUTES: Routes = [
  ...NAV_LINKS,
  { path: '', redirectTo: '/recommendations', pathMatch: 'full' },
  { path: '**', redirectTo: '/recommendations' }
];
