import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ParametersComparisonPlotComponent } from './parameters-comparison-plot.component';

describe('ParametersComparisonPlotComponent', () => {
  let component: ParametersComparisonPlotComponent;
  let fixture: ComponentFixture<ParametersComparisonPlotComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ParametersComparisonPlotComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ParametersComparisonPlotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
