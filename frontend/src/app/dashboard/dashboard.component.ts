import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import * as Chartist from 'chartist';
import { TableData } from '../models/table-data';

declare var $:any;
@Component({
    selector: 'dashboard-cmp',
    moduleId: module.id,
    templateUrl: 'dashboard.component.html'
})

//Zac, (1) data is loaded here to be used on charts in dashboard.components.html 
export class DashboardComponent implements OnInit{
    private numCrimes;
    //TODO
    private allCarsStolen: string[];

    constructor(private http: HttpClient){}


    ngOnInit(){

      //load crime count
      this.http.get<any>('http://perp-alb-1105201303.us-east-2.elb.amazonaws.com/api/v1/crimes/count?year_from=2000&year_to=2019').subscribe(data=>{
        data = data[0];
        this.numCrimes = data.num_collision+data.num_other+data.num_theft;
        console.log(data);
      });

      //load neighbourhoods where all cars stolen
      this.allCarsStolen = ['East Vancouver', 'Point Grey', 'West End'];














        var dataSales = {
          labels: ['2003', '2005', '2007', '2009', '2010', '2012', '2015', '2017'],
          series: [
             [287, 385, 490, 562, 594, 626, 698, 895, 952],
            [67, 152, 193, 240, 387, 435, 535, 642, 744],
            [23, 113, 67, 108, 190, 239, 307, 410, 410]
          ]
        };

        var optionsSales = {
          low: 0,
          high: 1000,
          showArea: true,
          height: "245px",
          axisX: {
            showGrid: false,
          },
          lineSmooth: Chartist.Interpolation.simple({
            divisor: 3
          }),
          showLine: true,
          showPoint: false,
        };

        var responsiveSales: any[] = [
          ['screen and (max-width: 640px)', {
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];

        new Chartist.Line('#chartHours', dataSales, optionsSales, responsiveSales);


        var data = {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          series: [
            [542, 543, 520, 680, 653, 753, 326, 434, 568, 610, 756, 895],
            [230, 293, 380, 480, 503, 553, 600, 664, 698, 710, 736, 795]
          ]
        };

        var options = {
            seriesBarDistance: 10,
            axisX: {
                showGrid: false
            },
            height: "245px"
        };

        var responsiveOptions: any[] = [
          ['screen and (max-width: 640px)', {
            seriesBarDistance: 5,
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              }
            }
          }]
        ];

        new Chartist.Line('#chartActivity', data, options, responsiveOptions);

        var dataPreferences = {
            series: [
                [25, 30, 20, 25]
            ]
        };

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

        new Chartist.Pie('#chartLang', dataPreferences, optionsPreferences);
        new Chartist.Pie('#chartLang', {
          labels: ['62%', '32%', '6%'],
          series: [62, 32, 6]
        });

        new Chartist.Pie('#chartPreferences', dataPreferences, optionsPreferences);

        new Chartist.Pie('#chartPreferences', {
          labels: ['62%','32%','6%'],
          series: [62, 32, 6]
        });
    }
}
