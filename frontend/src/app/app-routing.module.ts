import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RecommendationsComponent } from './recommendations/recommendations.component';
import { RmseComponent } from './rmse/rmse.component';
import {AlgorithmsComponent} from "./algorithms/algorithms.component";

const routes: Routes = [
  { path: '', redirectTo: '/recommendations', pathMatch: 'full' },
  { path: 'recommendations', component: RecommendationsComponent },
  { path: 'rmse', component: RmseComponent },
  { path: 'algorithms', component: AlgorithmsComponent}
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule { }
