import { Component, OnInit, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import * as Chart from 'chart.js';

import { RMSE } from '../model/rmse';
import { ApiData } from '../model/api-data';

@Component({
  selector: 'app-rmse',
  templateUrl: './rmse.component.html',
  styleUrls: ['./rmse.component.css']
})
export class RmseComponent implements OnInit {
  rmseHistory: RMSE[] = [];
  points = [];
  plot: Chart;

  constructor(private http: HttpClient, private elementRef: ElementRef) { }

  ngOnInit() {
    const url = 'http://127.0.0.1:5000/' + 'rmse/summary';

    this.http.get(url).subscribe(
      data => {
        console.log(data);
        this.rmseHistory = ((data as ApiData).data as Array<any>).map(jsonObject => new RMSE(jsonObject));

        for (const rmse of this.rmseHistory) {
          const x = new Date(rmse.timestamp * 1000);
          const y = rmse.rmse;
          this.points.push({x: x, y: y});
        }

        const ctx = this.elementRef.nativeElement.querySelector('#rmsePlot').getContext('2d');
        this.plot = new Chart(ctx, {
          type: 'line',
          data: {
            datasets: [{
              label: 'RMSE',
              data: this.points,
              backgroundColor: 'rgba(255,0,0,1)',
              borderColor: 'rgba(255,0,0,1)',
              fill: false
            }]
          },
          options: {
            scales: {
              xAxes: [{
                type: 'time',
                time: {
                  displayFormats: {
                    minute: 'YYYY-MM-DD HH:mm'
                  }
                }
              }]
            }
          }
        });
      },
      err => {
        console.log(err);
      }
    );
  }
}
