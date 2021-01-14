import { Component, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common';
import { ApiService } from '../api.service';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-request-form',
  templateUrl: './request-form.component.html',
  styleUrls: ['./request-form.component.css'],
  providers: [DatePipe, MessageService]
})
export class RequestFormComponent implements OnInit {

  DATE_FORMAT = 'yyyy-MM-dd';
  BASE_REQUEST_URL = 'http://127.0.0.1:5000/api/';
  defaultDate: Date = new Date(2003, 0, 1);

  selectedOption = "rate";

  date: any;
  parsedDate = "";

  dates: any;
  rangeDates: string[] = [];

  response: any;

  constructor(private datePipe: DatePipe, private apiService: ApiService, private messageService: MessageService) { }

  ngOnInit(): void {
  }

  submitDate(): void {
    const parsedDate = this.datePipe.transform(this.date, this.DATE_FORMAT);
    if (parsedDate !== null) {
      this.parsedDate = parsedDate;
      this.makeRequest();
    } else {
      this.messageService.add({
        severity: 'warn',
        summary: 'Please select date/dates from calendar'
      });
    }
  }

  submitRange(): void {
    this.rangeDates = [];
    if (this.dates === undefined) {
      this.messageService.add({
        severity: 'warn',
        summary: 'Please select date/dates from calendar'
      });
      return;
    }
    this.dates.forEach((date: Date) => {
      const parsedDate = this.datePipe.transform(date, this.DATE_FORMAT);
      if (parsedDate !== null) {
        this.rangeDates.push(parsedDate)
      } 
    });
    this.makeRequest();
  }

  makeRequest(): void {
    var requestURL: string = "";
    switch (this.selectedOption) {
      case 'rate': {
        requestURL = this.BASE_REQUEST_URL.concat('rates', '/', this.parsedDate);
        break;
      }
      case 'rates': {
        requestURL = this.BASE_REQUEST_URL.concat('rates', '/', this.rangeDates[0], '/', this.rangeDates[1]);
        break;
      }
      case 'sale': {
        requestURL = this.BASE_REQUEST_URL.concat('sales', '/', this.parsedDate);
        break;
      }
      case 'sales': {
        requestURL = this.BASE_REQUEST_URL.concat('sales', '/', this.rangeDates[0], '/', this.rangeDates[1]);
        break;
      }
    }

    this.apiService.getData(requestURL).then((data: any) => {
      this.response = data;
    }).catch((err) => {
      this.messageService.add({
        severity: 'error',
        summary: err['error']['error'] != null ? err['error']['error'] : 'Backend error occured. Please try again later'
      })
    });
  }
}
