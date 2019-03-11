import { Component, OnInit, Input } from '@angular/core';
import { TableData } from 'app/models/table-data';

@Component({
  selector: 'app-tablechart',
  templateUrl: './tablechart.component.html'
})
export class TablechartComponent implements OnInit {
  public pages = [];
  public pageIndex = 0;
  private pageSize = 10;
  goToPage(i){
    this.pageIndex = Math.max(i,0);
  }
  constructor() { }
  @Input() data: TableData;
  ngOnInit() {
    let rows = this.data.dataRows.slice();
    while(rows.length>0){
      let page = rows.splice(0, this.pageSize);
      this.pages.push(page);
    }
    console.log(this.pages);
  }

}
