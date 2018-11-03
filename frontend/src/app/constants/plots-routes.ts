import { Routes } from '@angular/router';
import { AlgorithmsComparisonPlotComponent } from '../components/plots/algorithms-comparison-plot/algorithms-comparison-plot.component';
import { ParametersComparisonPlotComponent } from '../components/plots/parameters-comparison-plot/parameters-comparison-plot.component';
import { TimeStepPlotComponent } from '../components/plots/time-step-plot/time-step-plot.component';
import { NavLink } from '../model/routing/nav-link';

export const PLOTS_NAV_LINKS: NavLink[] = [
  { path: 'alg', component: AlgorithmsComparisonPlotComponent, label: 'Algorithms Comparison' },
  { path: 'params', component: ParametersComparisonPlotComponent, label: 'Parameters Comparison' },
  { path: 'time_step', component: TimeStepPlotComponent, label: 'Time step' }
];

export const PLOTS_ROUTES: Routes = [
  { path: '', redirectTo: 'time_step', pathMatch: 'full' },
  ...PLOTS_NAV_LINKS,
  { path: '**', redirectTo: 'time_step' }
];
