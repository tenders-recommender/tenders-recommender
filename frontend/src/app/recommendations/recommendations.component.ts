import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Recommendation } from '../recommendation';
import { ApiData } from '../api-data';

@Component({
  selector: 'app-recommendations',
  templateUrl: './recommendations.component.html',
  styleUrls: ['./recommendations.component.css']
})
export class RecommendationsComponent implements OnInit {
  userId = 0;
  topN = 10;
  recommendations: Recommendation[] = [];

  constructor(private http: HttpClient) { }

  ngOnInit() {
  }

  onSubmit() {
    const url = 'http://127.0.0.1:5000/' + 'recommendations/' + this.userId + '?top=' + this.topN;

    this.http.get(url).subscribe(
      data => {
        console.log(data);
        this.recommendations = ((data as ApiData).data as Array<any>).map(jsonObject => new Recommendation(jsonObject));
      },
      err => {
        console.log(err);
      }
    );
  }
}
