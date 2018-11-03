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

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import { PlotsComponent } from './components/plots/plots.component';
import { RecommendationsComponent } from './components/recommendations/recommendations.component';
import { AlgorithmsComparisonPlotComponent } from './components/plots/algorithms-comparison-plot/algorithms-comparison-plot.component';
import { ParametersComparisonPlotComponent } from './components/plots/parameters-comparison-plot/parameters-comparison-plot.component';
import { TimeStepPlotComponent } from './components/plots/time-step-plot/time-step-plot.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    PlotsComponent,
    RecommendationsComponent,
    AlgorithmsComparisonPlotComponent,
    ParametersComparisonPlotComponent,
    TimeStepPlotComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    FormsModule,
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
