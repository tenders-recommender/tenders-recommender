import {Component, ElementRef, OnInit} from "@angular/core";
import * as Chart from 'chart.js';
import {Params} from "../model/params";
import {HttpClient} from "@angular/common/http";
import {ApiData} from "../model/api-data";

@Component({
  selector: 'app-rmse',
  templateUrl: './params.component.html',
  styleUrls: ['./params.component.css']
})
export class ParamsComponent implements OnInit {
  params: Params[] = [];
  plot: Chart;

  constructor(private http: HttpClient, private elementRef: ElementRef) {
  }

  ngOnInit(): void {
    const url = 'http://127.0.0.1:5000/' + 'param/comparison';

    this.http.get(url).subscribe(
      data => {
        this.params = ((data as ApiData).data as Array<any>).map(jsonObject => new Params(jsonObject));
        console.log(this.params)
        const dataSet = this.params.map(param => {
          return {
            'x': param.rmse,
            'y': param.time_elapsed
          }
        });

        const tooltips = this.params.map(param => {
          return [
            "k: " + param.k,
            "k_min: " + param.min_k,
            "min_support: " + param.simoptions.min_support,
            "name: " + param.simoptions.name,
            "user_based: " + param.simoptions.user_based
          ]
        });

        console.log(dataSet);

        const ctx = this.elementRef.nativeElement.querySelector('#paramsPlot').getContext('2d');


        let chartData = {
          labels: tooltips,
          datasets: [
            {
              label: "Time Elapsed",
              backgroundColor: "#8e5ea2",
              data: dataSet
            }
          ],
          other: tooltips

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
                    'Time:' + tooltipItem.yLabel].concat(data.labels[tooltipItem.index]);
                }
              }
            }
          }
        });


      }
    );


  }
}
