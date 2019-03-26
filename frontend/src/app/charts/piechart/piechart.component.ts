import { Component, OnInit, Input, ViewChild, ElementRef } from '@angular/core';
import * as Chartist from 'chartist';
import { PieData } from '../../models/pie-data';
@Component({
  selector: 'app-piechart',
  templateUrl: './piechart.component.html'
})
export class PiechartComponent implements OnInit{
  @ViewChild('chart') chart: ElementRef;
  @Input() pie : PieData;
  constructor() { }

  ngOnInit() {
  

    var optionsPreferences = {
      donut: true,
      donutWidth: 40,
      startAngle: 0,
      total: 100,
      showLabel: false,
      axisX: {
        showGrid: false
      }
    };

    // new Chartist.Pie(this.chart.nativeElement, this.pie.data, optionsPreferences);

    new Chartist.Pie(this.chart.nativeElement, this.pie.data);
  }

}
