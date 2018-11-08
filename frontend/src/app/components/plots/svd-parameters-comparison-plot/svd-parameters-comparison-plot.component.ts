import { Component, ElementRef, OnInit } from '@angular/core';
import * as Chart from 'chart.js';
import { ChartPoint } from 'chart.js';
import { SvdParametersComparisonData } from '../../../model/plots/svd-parameters-comparison-data';
import { ApiService } from '../../../services/api.service';

@Component({
  selector: 'app-svd-parameters-comparison-plot',
  templateUrl: './svd-parameters-comparison-plot.component.html',
  styleUrls: ['./svd-parameters-comparison-plot.component.scss']
})
export class SvdParametersComparisonPlotComponent implements OnInit {

  constructor(private readonly apiService: ApiService,
              private readonly elementRef: ElementRef) {
  }

  ngOnInit() {
    this.apiService.getSvdParametersComparisonData()
      .then(parametersComparisonData => this.createPlot(parametersComparisonData));
  }

  private createPlot(paramsData: SvdParametersComparisonData) {
    const dataSet: Array<ChartPoint> = [];

    for (let i = 0; i < paramsData.mean_test_rmse.length; i++) {
      dataSet.push({
        'x': paramsData.mean_fit_time[i] + paramsData.mean_test_time[i],
        'y': paramsData.mean_test_rmse[i]
      });
    }

    const tooltips = paramsData.params.map(param => {
      return [
        'n_factors: ' + param.n_factors,
        'n_epochs: ' + param.n_epochs,
        'biased: ' + param.biased,
        'init_mean: ' + param.init_mean,
        'init_std_dev: ' + param.init_std_dev,
        'lr_all: ' + param.lr_all,
        'reg_all: ' + param.reg_all
      ];
    });

    const ctx = this.elementRef.nativeElement
      .querySelector('#svdParamsPlot')
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
            label: (tooltipItem, data) => {
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
