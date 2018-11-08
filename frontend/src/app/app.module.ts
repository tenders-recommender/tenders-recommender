import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import {
  MatButtonModule,
  MatCardModule,
  MatDividerModule,
  MatFormFieldModule,
  MatIconModule,
  MatInputModule,
  MatPaginatorModule,
  MatTableModule,
  MatTabsModule,
  MatToolbarModule
} from '@angular/material';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FileDropModule } from 'ngx-file-drop';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import { AlgorithmsComparisonPlotComponent } from './components/plots/algorithms-comparison-plot/algorithms-comparison-plot.component';
import { KnnParametersComparisonPlotComponent } from './components/plots/knn-parameters-comparison-plot/knn-parameters-comparison-plot.component';
import { KnnTimeStepPlotComponent } from './components/plots/knn-time-step-plot/knn-time-step-plot.component';
import { PlotsComponent } from './components/plots/plots.component';
import { SvdParametersComparisonPlotComponent } from './components/plots/svd-parameters-comparison-plot/svd-parameters-comparison-plot.component';
import { SvdTimeStepPlotComponent } from './components/plots/svd-time-step-plot/svd-time-step-plot.component';
import { RecommendationsComponent } from './components/recommendations/recommendations.component';
import { TrainingComponent } from './components/training/training.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    PlotsComponent,
    RecommendationsComponent,
    AlgorithmsComparisonPlotComponent,
    KnnParametersComparisonPlotComponent,
    KnnTimeStepPlotComponent,
    SvdTimeStepPlotComponent,
    SvdParametersComparisonPlotComponent,
    TrainingComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    FormsModule,
    FileDropModule,
    MatToolbarModule,
    MatTabsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatDividerModule,
    MatIconModule,
    MatCardModule,
    MatTableModule,
    MatPaginatorModule
  ],
  providers: [],
  bootstrap: [
    AppComponent
  ]
})
export class AppModule {
}
