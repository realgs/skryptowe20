/* tslint:disable */
/* eslint-disable */

import { ExchangeRate, SaleData } from "@/api/TypeDefs";

interface HTTP {
	fetch(url: RequestInfo, init?: RequestInit): Promise<Response>;
}

export default class ApiClient {
	private _http: HTTP;
	private _apiUrl: string;

	constructor(apiUrl: string) {
		this._apiUrl = apiUrl;
		this._http = window as HTTP;
	}

	getExchangeRatesInRange(from: string, to: string): Promise<ExchangeRate[]> {
		const url = this._apiUrl + `api/exchangerates/?from=${from}&to=${to}`;

		const requestOptions = {
			method: "GET",
			headers: {
				Accept: "application/json"
			}
		} as RequestInit;

		return this._http
			.fetch(url, requestOptions)
			.then((response: Response) =>
				this.processGetExchangeRatesInRange(response)
			);
	}

	private processGetExchangeRatesInRange(
		response: Response
	): Promise<ExchangeRate[]> {
		if (response.status === 200) {
			return response.text().then(responseText => {
				const responseParsed = JSON.parse(
					responseText
				) as ExchangeRate[];
				return responseParsed;
			});
		}
		return Promise.resolve<ExchangeRate[]>(null as any);
	}

	getSalesInRange(from: string, to: string): Promise<SaleData[]> {
		const url = this._apiUrl + `api/sales/range/?from=${from}&to=${to}`;

		const requestOptions = {
			method: "GET",
			headers: {
				Accept: "application/json"
			}
		} as RequestInit;

		return this._http
			.fetch(url, requestOptions)
			.then((response: Response) =>
				this.processGetSalesInRange(response)
			);
	}

	private processGetSalesInRange(response: Response): Promise<SaleData[]> {
		if (response.status === 200) {
			return response.text().then(responseText => {
				const responseParsed = JSON.parse(responseText) as SaleData[];
				return responseParsed;
			});
		}
		return Promise.resolve<SaleData[]>(null as any);
	}
}
