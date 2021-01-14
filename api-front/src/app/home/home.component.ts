import { Component, OnInit } from '@angular/core';
import { Card } from '../card';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  cards: Card[] = [
    {
      type: "GET",
      url: "/api/rates/<date>",
      description: "Returns dict containing currency code and rate for specified date. Interpolated value means whether rate was given by NBP API or taken from previous/next day."
    },
    {
      type: "GET",
      url: "/api/rates/<start_date>/<end_date>",
      description: "Returns dict containing currency code and table of rates for specified period. Interpolated value means whether rate was given by NBP API or taken from previous/next day."
    },
    {
      type: "GET",
      url: "/api/sales/<date>",
      description: "Returns dict containing sale for specified date in USD and PLN"
    },
    {
      type: "GET",
      url: "/api/sales/<start_date>/<end_date>",
      description: "Returns dict containing sale for specified period in USD and PLN"
    },

  ]

  constructor() { }

  ngOnInit(): void {
  }

}
