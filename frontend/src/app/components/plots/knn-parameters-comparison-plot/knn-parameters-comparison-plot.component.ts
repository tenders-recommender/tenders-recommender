import { Component, ElementRef, OnInit } from '@angular/core';
import * as Chart from 'chart.js';
import { KnnParametersComparisonData } from '../../../model/plots/knn-parameters-comparison-data';
import { ApiService } from '../../../services/api.service';

@Component({
  selector: 'app-parameters-comparison-plot',
  templateUrl: './knn-parameters-comparison-plot.component.html',
  styleUrls: ['./knn-parameters-comparison-plot.component.scss']
})
export class KnnParametersComparisonPlotComponent implements OnInit {

  constructor(private readonly apiService: ApiService,
              private readonly elementRef: ElementRef) {
  }

  ngOnInit() {
    this.apiService.getKnnParametersComparisonData()
      .then(parametersComparisonData => this.createPlot(parametersComparisonData));
  }

  private createPlot(paramsData: ReadonlyArray<KnnParametersComparisonData>) {
    const dataSet = paramsData.map(param => {
      return {
        'x': param.time_elapsed,
        'y': param.rmse
      };
    });

    const tooltips = paramsData.map(param => {
      return [
        'k: ' + param.k,
        'k_min: ' + param.min_k,
        'min_support: ' + param.sim_options.min_support,
        'name: ' + param.sim_options.name,
        'user_based: ' + param.sim_options.user_based
      ];
    });

    const ctx = this.elementRef.nativeElement
      .querySelector('#knnParamsPlot')
      .getContext('2d');

    const chartData = {
      labels: tooltips,
      datasets: [
        {
          label: 'Test point',
          backgroundColor: '#8e5ea2',
          data: dataSet
        }
      ],
      other: tooltips

    };

    return new Chart(ctx, {
      type: 'scatter',
      data: chartData,
      options: {
        scales: {
          yAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: 'RMSE'
              },
              type: 'linear'
            }
          ],
          xAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: 'Time Elapsed'
              },
              type: 'linear'
            }
          ]
        },
        tooltips: {
          enabled: true,
          callbacks: {
            label: function (tooltipItem, data) {
              return [
                'Time:' + tooltipItem.xLabel,
                'RMSE:' + tooltipItem.yLabel
              ].concat(data.labels[tooltipItem.index]);
            }
          }
        }
      }
    });
  }

}
