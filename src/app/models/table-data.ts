//endpoint: https://host.com/api/table/<name> or https://host.com/api?table=<name>
export interface TableData {
	title: string;
	subtitle: string;
	headerRow: string[];
	dataRows: string[][];
}