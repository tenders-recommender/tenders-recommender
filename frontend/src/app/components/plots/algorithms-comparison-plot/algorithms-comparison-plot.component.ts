import { Component, ElementRef, OnInit } from '@angular/core';
import * as Chart from 'chart.js';
import { ChartPoint } from 'chart.js';
import * as math from 'mathjs';
import { AlgorithmsComparisonData } from '../../../model/plots/algorithms-comparison-data';
import { MeanStdPoint } from '../../../model/plots/mean-std-point';
import { ApiService } from '../../../services/api.service';

@Component({
  selector: 'app-algorithms-comparison-plot',
  templateUrl: './algorithms-comparison-plot.component.html',
  styleUrls: ['./algorithms-comparison-plot.component.scss']
})
export class AlgorithmsComparisonPlotComponent implements OnInit {

  constructor(private readonly apiService: ApiService,
              private readonly elementRef: ElementRef) {
  }

  ngOnInit() {
    this.apiService.getAlgorithmsComparisonData()
      .then(comparisonData => this.parsePoints(comparisonData))
      .then(points => this.createPlot(points));
  }

  groupBy<T, U>(list: ReadonlyArray<T>, keyGetter: (arg: T) => U) {
    const map = new Map<U, T[]>();

    list.forEach((item) => {
      const key = keyGetter(item);
      const collection = map.get(key);
      if (!collection) {
        map.set(key, [item]);
      } else {
        collection.push(item);
      }
    });

    return map;
  }

  private parsePoints(data: ReadonlyArray<AlgorithmsComparisonData>) {
    const points: MeanStdPoint[] = [];

    this.groupBy(data, arg => arg.algorithm)
      .forEach(((values, key) => {
        const timeElapsedArray = values.map(value => value.time_elapsed);
        const rmseArray = values.map(value => value.rmse);

        const timeElapsedMean = math.mean(timeElapsedArray);
        const timeElapsedStd = math.std(timeElapsedArray);

        const rmseMean = math.mean(rmseArray);
        const rmseStd = math.std(rmseArray);

        points.push({ label: key, xMean: timeElapsedMean, xStd: timeElapsedStd, yMean: rmseMean, yStd: rmseStd });
      }));

    return points;
  }

  private createPlot(meanStdPoints: MeanStdPoint[]) {
    const labels = meanStdPoints.map(meanStdPoint => meanStdPoint.label);

    const chartPoints = meanStdPoints.map(meanStdPoint => {
      return { x: meanStdPoint.xMean, y: meanStdPoint.yMean } as ChartPoint;
    });

    const ctx = this.elementRef.nativeElement
      .querySelector('#algPlot')
      .getContext('2d');

    return new Chart(ctx, {
      type: 'scatter',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Algorithm',
            data: chartPoints,
            backgroundColor: 'blue',
            fill: false
          },
        ]
      },
      options: {
        scales: {
          xAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: 'Time elapsed training and testing'
              },
              type: 'linear'
            }
          ],
          yAxes: [
            {
              scaleLabel: {
                display: true,
                labelString: 'RMSE'
              },
              type: 'linear'
            }
          ],
        },
        tooltips: {
          enabled: true,
          callbacks: {
            label: (tooltipItem, data) => ['RMSE:' + tooltipItem.yLabel, 'Time:' + tooltipItem.xLabel]
              .concat(['Algorithm: ' + data.labels[tooltipItem.index]])
          }
        }
      }
    });
  }
}
