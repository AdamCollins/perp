import { Component, OnInit } from '@angular/core';
import { TableData } from 'app/models/table-data';
import { HttpClient } from '@angular/common/http'

@Component({
    selector: 'table-cmp',
    moduleId: module.id,
    templateUrl: 'table.component.html'
})

export class TableComponent implements OnInit{
    public tableData1: TableData;
    public crimeData: TableData;
    constructor(private http: HttpClient){}


    getCrimeData(){

    }

    ngOnInit(){
        this.http.get('http://perp-alb-1105201303.us-east-2.elb.amazonaws.com/api/v1/table/Crime').subscribe(data => {
            //log api data for crime table
            let dataRows = [];
            //TODO replace with data param once cors is fixed.
            for (let x of this.api) {
                let row = [x.Crime_ID, x.NID, x.c_datetime, x.description];
                dataRows.push(row);
            }

            this.crimeData = {
                title: 'Crimes',
                subtitle: '',
                headerRow: ['ID', 'Neighbourhood ID', 'Time', 'Description'],
                dataRows: dataRows
            }
        });
        
        this.tableData1 = {
            title:'employees saLarIes',
            subtitle:'Employees salaries by country.',
            headerRow: [ 'ID', 'Name', 'Country', 'City', 'Salary'],
            dataRows: [
                ['1', 'Dakota Rice', 'Niger', 'Oud-Turnhout', '$36,738'],
                ['2', 'Minerva Hooper', 'Curaçao', 'Sinaai-Waas', '$23,789'],
                ['3', 'Sage Rodriguez', 'Netherlands', 'Baileux', '$56,142'],
                ['4', 'Philip Chaney', 'Korea, South', 'Overland Park', '$38,735'],
                ['5', 'Doris Greene', 'Malawi', 'Feldkirchen in Kärnten', '$63,542'],
                ['6', 'Mason Porter', 'Chile', 'Gloucester', '$78,615'], 
                ['1', 'Dakota Rice', 'Niger', 'Oud-Turnhout', '$36,738'],
                ['2', 'Minerva Hooper', 'Curaçao', 'Sinaai-Waas', '$23,789'],
                ['3', 'Sage Rodriguez', 'Netherlands', 'Baileux', '$56,142'],
                ['4', 'Philip Chaney', 'Korea, South', 'Overland Park', '$38,735'],
                ['5', 'Doris Greene', 'Malawi', 'Feldkirchen in Kärnten', '$63,542'],
                ['6', 'Mason Porter', 'Chile', 'Gloucester', '$78,615']
            ]
        };
    }


    public api = [{
        "Crime_ID": 1,
        "NID": 2,
        "c_datetime": "Tue, 04 Nov 2003 22:40:00 GMT",
        "description": "Vehicle Collision or Pedestrian Struck (with Injury)"
    }, {
        "Crime_ID": 2,
        "NID": 1,
        "c_datetime": "Sat, 15 Feb 2003 14:40:00 GMT",
        "description": "Vehicle Collision or Pedestrian Struck (with Injury)"
    }, {
        "Crime_ID": 3,
        "NID": 2,
        "c_datetime": "Tue, 01 Apr 2003 15:11:00 GMT",
        "description": "Vehicle Collision or Pedestrian Struck (with Injury)"
    }, {
        "Crime_ID": 4,
        "NID": 4,
        "c_datetime": "Tue, 01 Jul 2003 14:55:00 GMT",
        "description": "Vehicle Collision or Pedestrian Struck (with Injury)"
    }, {
        "Crime_ID": 5,
        "NID": 4,
        "c_datetime": "Mon, 20 Jan 2003 11:00:00 GMT",
        "description": "Vehicle Collision or Pedestrian Struck (with Injury)"
    }, {
        "Crime_ID": 6,
        "NID": 5,
        "c_datetime": "Tue, 25 Feb 2003 21:30:00 GMT",
        "description": "Theft of Bicycle"
    }, {
        "Crime_ID": 7,
        "NID": 2,
        "c_datetime": "Thu, 14 Aug 2003 10:20:00 GMT",
        "description": "Theft of Bicycle"
    }, {
        "Crime_ID": 8,
        "NID": 4,
        "c_datetime": "Sun, 10 Aug 2003 17:00:00 GMT",
        "description": "Theft of Vehicle"
    }, {
        "Crime_ID": 9,
        "NID": 5,
        "c_datetime": "Sun, 10 Aug 2003 17:00:00 GMT",
        "description": "Theft of Vehicle"
    }, {
        "Crime_ID": 10,
        "NID": 2,
        "c_datetime": "Thu, 17 Jul 2003 00:00:00 GMT",
        "description": "Theft of Vehicle"
    }]
}
