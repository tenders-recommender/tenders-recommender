import {Component, ElementRef, OnInit} from "@angular/core";
import * as Chart from 'chart.js';
import {Params} from "../model/params";
import {HttpClient} from "@angular/common/http";
import {ApiData} from "../model/api-data";
import {algorithm_list} from "../const/constants";

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
          return {
            'k': param.k,
            'k_min': param.min_k,
            'sim_optrions': param.simoptions
          }
        });

        console.log(dataSet);

        const ctx = this.elementRef.nativeElement.querySelector('#paramsPlot').getContext('2d');


        let chartData = {
          labels: algorithm_list,
          datasets: [
            {
              label: "Time Elapsed",
              backgroundColor: "#8e5ea2",
              data: dataSet
            }
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
            }
          }
        });


      }
    );


  }
}
