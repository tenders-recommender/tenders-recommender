import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { RMSE } from '../rmse';
import { ApiData } from '../api-data';

@Component({
  selector: 'app-rmse',
  templateUrl: './rmse.component.html',
  styleUrls: ['./rmse.component.css']
})
export class RmseComponent implements OnInit {
  rmseHistory: RMSE[] = [];

  constructor(private http: HttpClient) { }

  ngOnInit() {
    const url = 'http://127.0.0.1:5000/' + 'rmse/summary';

    this.http.get(url).subscribe(
      data => {
        console.log(data);
        this.rmseHistory = ((data as ApiData).data as Array<any>).map(jsonObject => new RMSE(jsonObject));
      },
      err => {
        console.log(err);
      }
    );
  }
}
