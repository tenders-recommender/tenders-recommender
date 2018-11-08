import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SvdParametersComparisonPlotComponent } from './svd-parameters-comparison-plot.component';

describe('SvdParametersComparisonPlotComponent', () => {
  let component: SvdParametersComparisonPlotComponent;
  let fixture: ComponentFixture<SvdParametersComparisonPlotComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SvdParametersComparisonPlotComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SvdParametersComparisonPlotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
