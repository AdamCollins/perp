export interface PieData {
	title:string;
	subtitle?:string;
	data:Data;
}
interface Data {
	series: number[];
	labels?: string[];
}
