import {Component, ElementRef, OnInit} from "@angular/core";
import * as Chart from 'chart.js';
import {HttpClient} from '@angular/common/http';
import {ApiData} from "../api-data";
import {Algorithm} from "../algorithm";
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
        console.log(data);
        const list = (data as ApiData).data as Array<any>;
        const grouped = this.groupBy(list, json => json.algorithm);
        this.results = algorithm_list.map(alg_name => this.createAlgorithm(grouped.get(alg_name)));
        const rmseAverage = [];
        const timeAverage = [];

        this.results.forEach(a => {
          rmseAverage.push(a.getAverageRmse());
          timeAverage.push(a.getAverageTimeElapsed());
        });

        const ctx = this.elementRef.nativeElement.querySelector('#algoPlot').getContext('2d');

        let chartData = {
          labels: algorithm_list,
          datasets: [
            {
              label: "Time Elapsed",
              backgroundColor: "blue",
              data: timeAverage
            },
            {
              label: "RMSE",
              backgroundColor: "red",
              data: rmseAverage
            }
          ]
        };

        this.plot = new Chart(ctx, {
          type: 'bar',
          data: chartData,
          options: {
            barValueSpacing: 20,
            scales: {
              yAxes: [{
                ticks: {
                  min: 0,
                }
              }]
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
