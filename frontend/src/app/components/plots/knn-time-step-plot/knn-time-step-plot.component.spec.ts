import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { KnnTimeStepPlotComponent } from './knn-time-step-plot.component';

describe('KnnTimeStepPlotComponent', () => {
  let component: KnnTimeStepPlotComponent;
  let fixture: ComponentFixture<KnnTimeStepPlotComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ KnnTimeStepPlotComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(KnnTimeStepPlotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
