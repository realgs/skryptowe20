import { Component, OnInit, Input, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.css']
})
export class TableComponent implements OnInit {

  @Input() tableData: any;
  headers: string[] = [];
  rows: any;

  constructor() { }

  ngOnInit(): void {
  }

  ngOnChanges(changes: SimpleChanges) {
    this.rows = this.tableData;
    this.headers = [];
    for (let key in this.tableData[0]) {
      if (this.tableData[0].hasOwnProperty(key)) {
        this.headers.push(key);
      }
    }
  }

}
