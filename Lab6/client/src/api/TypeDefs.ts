/* tslint:disable */
/* eslint-disable */

interface IExchangeRate {
	date: string;
	currency: string;
	interpolated: boolean;
}

export class ExchangeRate implements IExchangeRate {
	date!: string;
	currency!: string;
	interpolated!: boolean;

	init(data: any) {
		this.date = data["date"];
		this.currency = data["currency"];
		this.interpolated = data["interpolated"];
	}

	static fromJS(data: any): ExchangeRate {
		data = typeof data === "object" ? data : {};
		const result = new ExchangeRate();
		result.init(data);
		return result;
	}
}

interface ISaleData {
	date: string;
	USD: string;
	PLN: string;
}

export class SaleData implements ISaleData {
	date!: string;
	USD!: string;
	PLN!: string;

	init(data: any) {
		this.date = data["date"];
		this.USD = data["USD"];
		this.PLN = data["PLN"];
	}

	static fromJS(data: any): SaleData {
		data = typeof data === "object" ? data : {};
		const result = new SaleData();
		result.init(data);
		return result;
	}
}
