import { DatePipe } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { ChartDataSets } from 'chart.js';
import { Color, Label } from 'ng2-charts';
import { RequestService } from '../requests.service';




@Component({
  selector: 'app-exchange-rates',
  templateUrl: './exchange-rates.component.html',
  styleUrls: ['./exchange-rates.component.scss']
})
export class ExchangeRatesComponent implements OnInit, AfterViewInit {
  MIN_START_DATE = '2015-01-02'
  MAX_END_DATE = '2017-12-28'
  params: FormGroup
  dataSource = new MatTableDataSource<any>();
  displayedColumns = ['date', 'rate', 'interpolated']
  @ViewChild(MatPaginator) paginator: MatPaginator;
  lineChartData = [
    {
      data: [
      ]
     ,
      label: 'Usd rates over time',
      pointRadius: 5,
    },
  ];

  lineChartLabels: Label[] = [];

  lineChartOptions = {
    scales: {
      xAxes: [
       {
        barPercentage: 0.9,
        categoryPercentage: 0.55,
        type: "time",
        distribution: "linear",
        time: {
         unit: "day",
        },
       }
      ]
    },
    responsive: true,
    
  };

  lineChartColors: Color[] = [
    {
      borderColor: 'black',
      backgroundColor: 'rgba(255,255,0,0.28)',
    },
  ];

  lineChartLegend = true;
  lineChartPlugins = [];
  lineChartType = 'line';

  constructor(private reqService: RequestService, private datePipe: DatePipe, private http: HttpClient) {
    
   }

  ngOnInit(): void {
    this.params = new FormGroup({
      startDate: new FormControl('', Validators.required),
      endDate: new FormControl('', Validators.required),
      currency: new FormControl(),
    });
  }

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    
  }

  fillChartWithData() {
    let tempArr = []
    this.lineChartLabels = []
    this.dataSource.data.forEach(element => {
      tempArr.push({x : element.daterate, y: element.rate})
      this.lineChartLabels.push( element.daterate)
    });
    this.lineChartData[0].data = tempArr;
  }

  getExchangerates(){
    let startDate = this.datePipe.transform(this.params.get('startDate')?.value, 'yyyy-MM-dd');
    let endDate =  this.datePipe.transform(this.params.get('endDate')?.value, 'yyyy-MM-dd');
    let apiUrl = `http://127.0.0.1:5000/exchangerates?startDate=${startDate}&endDate=${endDate}`;
    this.http.get(apiUrl).subscribe(rates => { this.dataSource.data = rates as Array<any>; this.fillChartWithData()})

  }

}
