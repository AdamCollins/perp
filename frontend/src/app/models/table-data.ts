//API: 		host.com/api/table/{tablename}?rows={# of rows}&sortby={col name}
//Returns: headerRow, dataRows.
//Defaults: 
//		- Without rows return all rows
//		- Without sortby don't sort
export interface TableData {
	title: string;
	subtitle: string;

	headerRow: string[];
	dataRows: string[][];
}