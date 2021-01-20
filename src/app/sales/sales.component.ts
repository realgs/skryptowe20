import { DatePipe } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatTableDataSource } from '@angular/material/table';
import { ChartDataSets, ChartOptions, ChartType } from 'chart.js';
import { Color, Label } from 'ng2-charts';
import { RequestService } from '../requests.service';

@Component({
  selector: 'app-sales',
  templateUrl: './sales.component.html',
  styleUrls: ['./sales.component.scss']
})
export class SalesComponent implements OnInit {
  MAX_END_DATE = '2017-12-24'
  MIN_START_DATE = '2015-01-04'
  date: FormControl
  saleData: any
  barChartOptions: ChartOptions = {
    responsive: true,
  };
  barChartLabels: Label[] = ['in USD', 'in PLN'];
  barChartType: ChartType = 'bar';
  barChartLegend = true;
  barChartPlugins = [];

  barChartData: ChartDataSets[] = [
    { data: [] }
  ];


  myFilter = (d: Date | null): boolean => {
    const day = (d || new Date()).getDay();
    return day == 0;
  }
  constructor(private reqService: RequestService, private datePipe: DatePipe) { }

  ngOnInit(): void {
      this.date = new FormControl('', Validators.required)
  }


  getSaleData() {
    let daySelected =  this.datePipe.transform(this.date.value, 'yyyy-MM-dd');
    let apiUrl = `http://127.0.0.1:5000/transactions?day=${daySelected}`;
    this.reqService.fetchSaleData(apiUrl).subscribe(fetchedData =>{this.saleData = fetchedData; console.log(fetchedData); this.populateChart(fetchedData) })
  }


  populateChart(saleData: any){
    this.barChartData[0].data = []
    this.barChartData[0].data.push(saleData.usdAmount);
    this.barChartData[0].data.push(saleData.plnAmount);
    this.barChartData[0].label = `Money spent on avocados in ${saleData.date}`;
  }

}
