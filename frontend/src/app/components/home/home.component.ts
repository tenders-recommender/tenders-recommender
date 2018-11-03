import { Component, OnInit } from '@angular/core';
import { Routes } from '@angular/router';
import { NAV_LINKS } from '../../constants/routes';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  readonly navLinks: Routes;

  constructor() {
    this.navLinks = NAV_LINKS;
  }

  ngOnInit() {
  }

}
