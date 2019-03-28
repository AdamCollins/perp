import {
  Component,
  OnInit,
  Input
} from '@angular/core';
import {
  TableData
} from 'app/models/table-data';

@Component({
  selector: 'app-tablechart',
  templateUrl: './tablechart.component.html'
})
export class TablechartComponent implements OnInit {
  public pages = [];
  public pageIndex = 0;
  public pageSize = 10;
  private isLoaded = false;
  nextPage(i) {
    this.pageIndex += i
  }
  goToPage(i) {
    this.pageIndex = i
    console.log(i);
  }
  constructor() {}
  @Input() data: TableData;
  @Input() size: number;
  ngOnInit() {
    if (this.size) {
      this.pageSize = this.size;
    }
      let rows = this.data.dataRows.slice();
      while (rows.length > 0) {
        let page = rows.splice(0, this.pageSize);
        this.pages.push(page);
      }
  }
}
