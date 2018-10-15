import {Component, ElementRef, OnInit} from "@angular/core";
import * as Chart from 'chart.js';
import {HttpClient} from '@angular/common/http';
import {ApiData} from "../model/api-data";
import {Algorithm} from "../model/algorithm";
import {algorithm_list} from "../const/constants";


@Component({
  selector: 'app-rmse',
  templateUrl: './algorithms.component.html',
  styleUrls: ['./algorithms.component.css']
})
export class AlgorithmsComponent implements OnInit {
  results: Algorithm[] = [];
  plot: Chart;

  constructor(private http: HttpClient, private elementRef: ElementRef) {
  }

  ngOnInit(): void {
    const url = 'http://127.0.0.1:5000/' + 'alg/comparison';

    this.http.get(url).subscribe(
      data => {
        const list = (data as ApiData).data as Array<any>;
        const grouped = this.groupBy(list, json => json.algorithm);
        this.results = algorithm_list.map(alg_name => this.createAlgorithm(grouped.get(alg_name)));
        const dataSet = [];

        this.results.forEach(a => {
          dataSet.push({'x': a.getAverageRmse(), 'y': a.getAverageTimeElapsed()});
        });

        const ctx = this.elementRef.nativeElement.querySelector('#algoPlot').getContext('2d');

        let chartData = {
          labels: algorithm_list,
          datasets: [
            {
              label: "Algorithm",
              backgroundColor: "blue",
              data: dataSet
            },
          ]
        };

        this.plot = new Chart(ctx, {
          type: 'scatter',
          data: chartData,
          options: {
            scales: {
              yAxes: [{
                scaleLabel: {
                  display: true,
                  labelString: 'Time Elapsed'
                },
                type: 'linear'
              }],
              xAxes: [{
                scaleLabel: {
                  display: true,
                  labelString: 'RMSE'
                },
                type: 'linear'
              }]
            },
            tooltips: {
              enabled: true,
              callbacks: {
                label: function (tooltipItem, data) {
                  return ['RMSE:' + tooltipItem.xLabel,
                    'Time:' + tooltipItem.yLabel].concat(["Algorithm: " + data.labels[tooltipItem.index]])
                }
              }
            }
          }
        });

      }
    );

  }

  groupBy(list, keyGetter) {
    const map = new Map();
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

  createAlgorithm(list: Array<any>): Algorithm {
    const name = list[0].algorithm;
    const rmse = [];
    const time_elapsed = [];

    list.forEach(i => {
      rmse.push(i.rmse);
      time_elapsed.push(i.time_elapsed)
    });

    return new Algorithm(name, rmse, time_elapsed)

  }

}
