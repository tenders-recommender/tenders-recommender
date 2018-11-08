import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { KnnParametersComparisonPlotComponent } from './knn-parameters-comparison-plot.component';

describe('KnnParametersComparisonPlotComponent', () => {
  let component: KnnParametersComparisonPlotComponent;
  let fixture: ComponentFixture<KnnParametersComparisonPlotComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ KnnParametersComparisonPlotComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(KnnParametersComparisonPlotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
