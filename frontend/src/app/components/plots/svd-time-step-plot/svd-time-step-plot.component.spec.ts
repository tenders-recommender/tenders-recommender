import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SvdTimeStepPlotComponent } from './svd-time-step-plot.component';

describe('SvdTimeStepPlotComponent', () => {
  let component: SvdTimeStepPlotComponent;
  let fixture: ComponentFixture<SvdTimeStepPlotComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SvdTimeStepPlotComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SvdTimeStepPlotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
