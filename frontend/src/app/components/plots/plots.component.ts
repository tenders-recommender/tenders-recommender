import { Component, OnInit } from '@angular/core';
import { Routes } from '@angular/router';
import { PLOTS_NAV_LINKS } from '../../constants/plots-routes';

@Component({
  selector: 'app-plots',
  templateUrl: './plots.component.html',
  styleUrls: ['./plots.component.scss']
})
export class PlotsComponent implements OnInit {
  readonly navLinks: Routes;

  constructor() {
    this.navLinks = PLOTS_NAV_LINKS;
  }

  ngOnInit() {
  }
}
