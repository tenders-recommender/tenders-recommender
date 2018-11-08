import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator, MatTableDataSource } from '@angular/material';
import { Recommendation } from '../../model/recommendation';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-recommendations',
  templateUrl: './recommendations.component.html',
  styleUrls: ['./recommendations.component.scss']
})
export class RecommendationsComponent implements OnInit {
  @ViewChild(MatPaginator) paginator: MatPaginator;
  public userID: number;
  public topN: number;
  public dataSource: MatTableDataSource<Recommendation>;

  constructor(private readonly apiService: ApiService) {
  }

  ngOnInit() {
    this.dataSource = new MatTableDataSource<Recommendation>([]);
    this.dataSource.paginator = this.paginator;
  }

  getRecommendations(): void {
    const recommendationsPromise = this.topN
      ? this.apiService.getRecommendations(this.userID, this.topN)
      : this.apiService.getRecommendations(this.userID);

    recommendationsPromise.then(recommendations => {
      this.dataSource.data = [...recommendations];
    });
  }
}
