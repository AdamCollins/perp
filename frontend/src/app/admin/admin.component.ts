import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { HttpErrorResponse } from '@angular/common/http';
import * as Chartist from 'chartist';
import { PieData } from '../models/pie-data';
import { catchError, retry } from 'rxjs/operators';
import { _throw } from 'rxjs/observable/throw';
declare var $: any;


const httpOptions = {
	headers: new HttpHeaders({
		'Accept': 'application/json',
		'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, DELETE, PUT',
		'Access-Control-Allow-Origin': '*'
	})
}

@Component({
	selector: 'app-admin',
	templateUrl: './admin.component.html'
})
export class AdminComponent implements OnInit {

	usersActive: number;
	usersTotal: number;
	neighbourhoods = ['Arbutus-Ridge', 'Downtown', 'Dunbar-Southlands', 'Fairview', 'Grandview-Woodland', 'Hastings-Sunrise', 'Kensington-Cedar Cottage', 'Kerrisdale', 'Killarney', 'Kitsilano', 'Marpole', 'Mount Pleasant', 'Oakridge', 'Renfrew-Collingwood', 'Riley Park', 'Shaughnessy', 'South Cambie', 'Strathcona', 'Sunset', 'Victoria-Fraserview', 'West End'];
	pie: PieData;

	constructor(private http: HttpClient) { }



	private handleAdd(form: any) {
		console.log('handled');
		// let msg = 'Incorrect username or password';
		// let status = 'danger';
		// let icon = 'ti-thumb-down';
		if (form.password == 'thebeesknees') {
			if (form.update) {
				this.http.get<Object>(`http://perp-alb-1105201303.us-east-2.elb.amazonaws.com/api/v1/criminal/update/${form.cid}?age=${form.age}&height_cm=${form.height}&hair_color=${form.hair}&lives_in=${form.neighbourhood}`)
					.subscribe((data) => {
						console.log('data', data);
						this.notify('Update Sucessfully!', 'success');
					}, (err) => {
						console.log('Error:');
						console.log(err.error);
						console.log(err.name);
						console.log(err.message);
						console.log(err.status);
						this.notify('Add Failed. Missing a Field? 😥', 'danger');
					});
			} else {
				this.http.get<Object>(`http://perp-alb-1105201303.us-east-2.elb.amazonaws.com/api/v1/criminal/add?age=${form.age}&height_cm=${form.height}&hair_color=${form.hair}&lives_in=${form.neighbourhood}`)
					.subscribe((data) => {
						console.log('data', data);
						this.notify('Added Sucessfully!', 'success');
					}, (err) => {
						console.log('Error:');
						console.log(err.error);
						console.log(err.name);
						console.log(err.message);
						console.log(err.status);
						this.notify('Add Failed. Missing a Field? 😥', 'danger');
					});
			}
		} else {
			//Password incorrect
			this.notify('Username or Password Incorrect 👹', 'danger');
		}
	}


	private handleDelete(form: any) {
		if (form.password == 'thebeesknees') {
			this.http.get<Object>(`http://perp-alb-1105201303.us-east-2.elb.amazonaws.com/api/v1/criminal/delete/${form.cid}`)
				.subscribe((data) => {
					console.log('data', data);
					this.notify('Deleted Sucessfully!', 'success');
				}, (err) => {
					console.log('Error:');
					console.log(err.error);
					console.log(err.name);
					console.log(err.message);
					console.log(err.status);
					this.notify('Delete Failed. Missing a Field? 😥', 'danger');
				});
		} else {
				
		}
	}


	private notify(msg, status) {
		let icon = (status == 'success') ? 'ti-thumb-up' : 'ti-thumb-down';

		$.notify({
			icon: icon,
			message: msg
		}, {
				type: status,
				timer: 3000,
				placement: {
					from: 'top',
					align: 'right'
				}
			});
	}

	ngOnInit() {
		this.usersActive = 1;
		this.usersTotal = 13;
		var dataSales = {
			labels: ['9:00AM', '12:00AM', '3:00PM', '6:00PM', '9:00PM', '12:00PM', '3:00AM', '6:00AM'],
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



		//Editing this changes the data used build the pie chart
		this.pie = {
			title: 'User Locations',
			subtitle: 'By country',
			data: {
				labels: ['62%', '22%', '6%', '10%'],
				series: [62, 22, 6, 10]
			}
		};


	}
}
