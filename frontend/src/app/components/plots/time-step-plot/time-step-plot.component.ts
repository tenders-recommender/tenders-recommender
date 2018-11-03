import { Component, ElementRef, OnInit } from '@angular/core';
import * as Chart from 'chart.js';
import { ChartDataSets, ChartPoint, ChartXAxe } from 'chart.js';
import { TimeStepData } from '../../../model/plots/time-step-data';
import { ApiService } from '../../../services/api.service';

enum PlotType {
  TIMESTAMP = 'Timestamp',
  INTERACTIONS = 'Interactions'
}

@Component({
  selector: 'app-time-step-plot',
  templateUrl: './time-step-plot.component.html',
  styleUrls: ['./time-step-plot.component.scss']
})
export class TimeStepPlotComponent implements OnInit {

  public PlotType = PlotType;

  private timestampPoints: ChartPoint[];
  private interactionsPoints: ChartPoint[];

  private currentPlotType: PlotType;

  constructor(private readonly apiService: ApiService,
              private readonly elementRef: ElementRef) {
  }

  ngOnInit() {
    this.apiService.getTimeStepData()
      .then(timeStepData => this.parsePoints(timeStepData))
      .then(() => this.createBothPlots())
      .then(() => this.currentPlotType = PlotType.TIMESTAMP);
  }

  public changePlot() {
    if (this.currentPlotType === PlotType.TIMESTAMP) {
      this.currentPlotType = PlotType.INTERACTIONS;
      this.createInteractionsPlot();
    } else {
      this.currentPlotType = PlotType.TIMESTAMP;
      this.createTimestampPlot();
    }
  }

  private parsePoints(data: ReadonlyArray<TimeStepData>) {
    const timestampPoints: ChartPoint[] = [];
    const interactionsPoints: ChartPoint[] = [];

    for (const datum of data) {
      const timestampX = new Date(datum.earlier_than * 1000);
      const interactions = datum.interactions;
      const y = datum.rmse;

      timestampPoints.push({ x: timestampX, y: y });
      interactionsPoints.push({ x: interactions, y: y });
    }

    this.timestampPoints = timestampPoints;
    this.interactionsPoints = interactionsPoints;
  }

  private createBothPlots() {
    this.createTimestampPlot();
    this.createInteractionsPlot();
  }

  private createTimestampPlot() {
    this.createPlot('#timestampPlot',
      {
        label: 'RMSE',
        xAxisID: 'timestamp',
        data: this.timestampPoints,
        backgroundColor: '#E74C3C',
        borderColor: '#E74C3C',
        fill: false
      },
      {
        id: 'timestamp',
        scaleLabel: {
          display: true,
          labelString: 'Timestamp'
        },
        type: 'time',
        time: {
          displayFormats: {
            minute: 'YYYY-MM-DD HH:mm'
          }
        }
      });
  }

  private createInteractionsPlot() {
    this.createPlot('#interactionsPlot',
      {
        label: 'RMSE',
        xAxisID: 'interactions',
        data: this.interactionsPoints,
        backgroundColor: '#2ECC71',
        borderColor: '#2ECC71',
        fill: false
      },
      {
        id: 'interactions',
        scaleLabel: {
          display: true,
          labelString: 'Interactions amount'
        },
        type: 'linear'
      });
  }

  private createPlot(canvasId: string, dataset: ChartDataSets, xAxe: ChartXAxe): Chart {
    const ctx = this.elementRef.nativeElement
      .querySelector(canvasId)
      .getContext('2d');

    return new Chart(ctx, {
      type: 'line',
      data: {
        datasets: [
          dataset
        ]
      },
      options: {
        scales: {
          xAxes: [
            xAxe
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
        }
      }
    });
  }

}
