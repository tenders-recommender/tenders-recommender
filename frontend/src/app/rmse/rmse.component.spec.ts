import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RmseComponent } from './rmse.component';

describe('RmseComponent', () => {
  let component: RmseComponent;
  let fixture: ComponentFixture<RmseComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RmseComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RmseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
