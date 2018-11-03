import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TimeStepPlotComponent } from './time-step-plot.component';

describe('TimeStepPlotComponent', () => {
  let component: TimeStepPlotComponent;
  let fixture: ComponentFixture<TimeStepPlotComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TimeStepPlotComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TimeStepPlotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
