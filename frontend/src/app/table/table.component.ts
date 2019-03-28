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
    crimeData: TableData;
    criminalData: TableData;
    neighbourhoodData: TableData;
    demoData: TableData;


    neighLoaded:Boolean;
    crimeLoaded: Boolean;
    criminalLoaded: Boolean;
    demosLoaded: Boolean;


    constructor(private http: HttpClient){}


    getCrimeData(){

    }

    ngOnInit(){

        //Crime
        this.http.get<any[]>('http://perp-alb-1105201303.us-east-2.elb.amazonaws.com/api/v1/table/Crime?page_size=50&page=0').subscribe((data)=> {
            //log api data for crime table
            let dataRows = [];
            console.log(data);
            
            //TODO replace with data param once cors is fixed.
            for (let x of data) {
                let row = [x.Crime_ID, x.NID, x.c_datetime, x.description];
                dataRows.push(row);
            }

            this.crimeData = {
                title: 'Crimes',
                subtitle: '',
                headerRow: ['ID', 'Neighbourhood ID', 'Time', 'Description'],
                dataRows: dataRows
            }
            this.crimeLoaded = true;
        }, err => {console.log(err)});

        //TODO Criminals
        this.http.get<any[]>('http://perp-alb-1105201303.us-east-2.elb.amazonaws.com/api/v1/table/Criminal?page_size=50&page=0').subscribe((data) => {
            //log api data for crime table
            let dataRows = [];
            console.log(data);

            //TODO replace with data param once cors is fixed.
            for (let x of data) {
                let row = [x.Criminal_ID, x.age, x.hair_color, x.height_cm, x.lives_in];
                dataRows.push(row);
            }

            this.criminalData = {
                title: 'Criminals',
                subtitle: '',
                headerRow: ['ID', 'Age', 'Hair Colour', 'Height(cm)', 'Neighbourhood (NID)'],
                dataRows: dataRows
            }
            this.criminalLoaded = true;
        }, err => { console.log(err) });
        //Neighbourhood
        this.http.get<any []>('http://perp-alb-1105201303.us-east-2.elb.amazonaws.com/api/v1/table/Neighbourhood').subscribe((data) => {
            //log api data for crime table
            let dataRows = [];
            //TODO replace with data param once cors is fixed.

            for (let x of data) {
                let row = [x.n_name, x.NID, x.DID];
                dataRows.push(row);
            }
            this.neighbourhoodData = {
                title: 'Neighbourhood',
                subtitle: '',
                headerRow: ['Name', 'Neighbourhood ID', 'Demographic ID'],
                dataRows: dataRows
            }
            
            this.neighLoaded = true;
        }, err => { console.log(err) });

        //Demographics
        this.http.get<any[]>('http://perp-alb-1105201303.us-east-2.elb.amazonaws.com/api/v1/table/Demographic').subscribe((data) => {
            //log api data for crime table
            let dataRows = [];
            //TODO replace with data param once cors is fixed.

            for (let x of data) {
                let row = [x.DID, x.population, x.num_old, x.num_old, x.primary_language, x.secondary_language, x.third_language];
                dataRows.push(row);
            }
            this.demoData = {
                title: 'Demographics',
                subtitle: '',
                headerRow: ['Demographic ID', 'Population', 'Number of Youth (<25)', 'Number of seniors(>65)', 'Primary Language', 'Secondary Language', 'Third Language'],
                dataRows: dataRows
            }
            this.demosLoaded = true;
        }, err => { console.log(err) });



    }

}


/*
DID	9
num_old	20040
num_young	23010
population	43050
primary_language	"English"
secondary_language	"Mandarin"
third_language	"French"

*/