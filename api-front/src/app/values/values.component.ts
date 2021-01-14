import { Component, OnInit, Input, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-values',
  templateUrl: './values.component.html',
  styleUrls: ['./values.component.css']
})
export class ValuesComponent implements OnInit {

  @Input() response: any;

  @Input() requestType = "";

  chartData: any;
  tableData: any;

  constructor() { }

  ngOnInit(): void {
  }

  ngOnChanges(changes: SimpleChanges) {
    if (!changes['response']) {
      return;
    }

    if (this.response !== undefined) {
      let labels: string[] = [];
      let dataset: number[] = [];
      this.chartData = null;
      if (this.requestType === "rates" || this.requestType === "rate") {
        this.tableData = this.response.rates;
        for (let i = 0; i < this.response.rates.length; i++) {
          labels.push(this.response.rates[i]["date"]);
          dataset.push(this.response.rates[i]["rate"]);
        }
        if (this.response.rates.length > 1) {
          this.buildRatesChart(labels, dataset);
        }
      } 
      else {
        this.tableData = this.response.sale;
        let secondDataset: number[] = [];
        for (let i = 0; i < this.response.sale.length; i++) {
          labels.push(this.response.sale[i]["date"]);
          dataset.push(this.response.sale[i]["usd_sale"]);
          secondDataset.push(this.response.sale[i]["pln_sale"]);
        }
        if (this.response.sale.length > 1) {
          this.buildSalesChart(labels, dataset, secondDataset);
        }
      }
    }
  }

  buildRatesChart(labels: string[], dataset: number[]) {
    this.chartData = {
      labels: labels,
      datasets: [
        {
          label: 'USD',
          data: dataset,
          fill: false,
          borderColor: '#2196F3'
        }
      ]
    }
  }

  buildSalesChart(labels: string[], firstDataset: number[], secondDataset: number[]) {
    this.chartData = {
      labels: labels,
      datasets: [
          {
              label: 'USD',
              data: firstDataset,
              fill: false,
              borderColor: '#2196F3'
          },
          {
              label: 'PLN',
              data: secondDataset,
              fill: false,
              borderColor: '#FFD700'
          }
      ]
  }
  }
}
