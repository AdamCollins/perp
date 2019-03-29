import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import * as Chartist from 'chartist';
import { TableData } from '../models/table-data';
import { PieData } from '../models/pie-data';
import { map } from 'rxjs/operators';


declare var $:any;
const str = (n) => '' + n;
@Component({
    selector: 'dashboard-cmp',
    moduleId: module.id,
    templateUrl: 'dashboard.component.html'
})

//Zac, (1) data is loaded here to be used on charts in dashboard.components.html 
export class DashboardComponent implements OnInit{
    private numCrimes = [0];
    private index = 0;
    private sumOfStolen: number;
    private allCarsStolen: TableData;
    private carsLoaded = false;
    private pie: PieData;
    private criminalProps = [];
    constructor(private http: HttpClient){}


    crimeSelectChange(month : number){
      this.index = month;
      console.log('called');
    }

  criminalProperiesChange(column : string){
    this.http.get<any[]>(`http://perp-alb-1105201303.us-east-2.elb.amazonaws.com/api/v1/criminal/column/${column}?page=0&page_size=8`).subscribe(data => {
      this.criminalProps = data.map((x)=>x[column]);
      console.log(this.criminalProps);
      
    });
  }

    ngOnInit(){

      this.criminalProperiesChange('hair_color');

      //load crime count
      this.http.get<any[]>('http://perp-alb-1105201303.us-east-2.elb.amazonaws.com/api/v1/theft/car/all').subscribe(data=>{
        this.allCarsStolen = {
          title: 'Don\'t park your car here',
          subtitle: 'These neighbourhoods have had all type of car stolen.',
          headerRow: ['Neighbourhood'],
          dataRows: data.map(x=>[x.n_name])
        }
        this.carsLoaded = true;
      });

      //load neighbourhoods where all cars stolen
        //http://perp-alb-1105201303.us-east-2.elb.amazonaws.com/api/v1/theft/car/all



      var dataSales = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Nov', 'Dec'],
        series: [
          [287, 385, 490, 562, 594, 626, 698, 895, 952],
          [67, 152, 193, 240, 387, 435, 535, 642, 744],
          [23, 113, 67, 108, 190, 239, 307, 410, 410]
        ]
      };

      var optionsSales = {
        low: 0,
        high: 1800,
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

      this.http.get<any []>('http://perp-alb-1105201303.us-east-2.elb.amazonaws.com/api/v1/crimes/count?month_from=0&month_to=12').subscribe(data => {
        console.log(data);
        let colli = [];
        let theft = [];
        let other = []; 
        for(let x of data){
          colli.push(x.num_collision);
          theft.push(x.num_theft);
          other.push(x.num_other);

          //build month map
          this.numCrimes.push(x.num_collision + x.num_theft + x.num_other);
        }
        dataSales.series = [theft, other, colli];
        new Chartist.Line('#chartHours', dataSales, optionsSales, responsiveSales);

        this.numCrimes[0] = (colli.concat(theft,other)).reduce((acc, n)=>acc+n);
        let crime_percentages = 
          {
            collisions: colli.reduce((acc,n)=>acc+n)/this.numCrimes[0],
            theft: theft.reduce((acc, n) => acc + n) / this.numCrimes[0],
            other: other.reduce((acc, n) => acc + n) / this.numCrimes[0],
          }

        new Chartist.Pie('#chartPreferences', dataPreferences, optionsPreferences);

        new Chartist.Pie('#chartPreferences', {
          labels: [Math.round(crime_percentages.theft * 100) + '%', 
                  Math.round(crime_percentages.other* 100) + '%',
                  Math.round(crime_percentages.collisions*100) + '%'],
          series: [crime_percentages.theft, crime_percentages.other, crime_percentages.collisions,]
        });
      });


      //Stolen Item
      this.http.get<any[]>('http://perp-alb-1105201303.us-east-2.elb.amazonaws.com/api/v1/table/Item').subscribe((data) => {
        //log api data for crime table
        let sum = 0;
        for (let x of data){
          sum += x.i_value;
        }
        this.sumOfStolen = sum;
      }, err => { console.log(err) });



       


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


    }
}
