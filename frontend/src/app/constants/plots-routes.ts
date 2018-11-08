import { Routes } from '@angular/router';
import { AlgorithmsComparisonPlotComponent } from '../components/plots/algorithms-comparison-plot/algorithms-comparison-plot.component';
import { KnnParametersComparisonPlotComponent } from '../components/plots/knn-parameters-comparison-plot/knn-parameters-comparison-plot.component';
import { KnnTimeStepPlotComponent } from '../components/plots/knn-time-step-plot/knn-time-step-plot.component';
import { SvdParametersComparisonPlotComponent } from '../components/plots/svd-parameters-comparison-plot/svd-parameters-comparison-plot.component';
import { SvdTimeStepPlotComponent } from '../components/plots/svd-time-step-plot/svd-time-step-plot.component';
import { NavLink } from '../model/routing/nav-link';

export const PLOTS_NAV_LINKS: NavLink[] = [
  { path: 'alg', component: AlgorithmsComparisonPlotComponent, label: 'Algorithms Comparison' },
  { path: 'knn_params', component: KnnParametersComparisonPlotComponent, label: 'KNN Parameters Comparison' },
  { path: 'knn_time_step', component: KnnTimeStepPlotComponent, label: 'KNN Time step' },
  { path: 'svd_params', component: SvdParametersComparisonPlotComponent, label: 'SVD Parameters Comparison' },
  { path: 'svd_time_step', component: SvdTimeStepPlotComponent, label: 'SVD Time step' }
];

export const PLOTS_ROUTES: Routes = [
  { path: '', redirectTo: 'svd_time_step', pathMatch: 'full' },
  ...PLOTS_NAV_LINKS,
  { path: '**', redirectTo: 'svd_time_step' }
];
