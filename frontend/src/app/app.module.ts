import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { RecommendationsComponent } from './recommendations/recommendations.component';
import { RmseComponent } from './rmse/rmse.component';
import { AppRoutingModule } from './app-routing.module';
import {AlgorithmsComponent} from "./algorithms/algorithms.component";
import {ParamsComponent} from "./params/params.component";

@NgModule({
  declarations: [
    AppComponent,
    RecommendationsComponent,
    RmseComponent,
    AlgorithmsComponent,
    ParamsComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
