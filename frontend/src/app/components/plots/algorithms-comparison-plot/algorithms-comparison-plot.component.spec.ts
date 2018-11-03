import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AlgorithmsComparisonPlotComponent } from './algorithms-comparison-plot.component';

describe('AlgorithmsComparisonPlotComponent', () => {
  let component: AlgorithmsComparisonPlotComponent;
  let fixture: ComponentFixture<AlgorithmsComparisonPlotComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AlgorithmsComparisonPlotComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlgorithmsComparisonPlotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
