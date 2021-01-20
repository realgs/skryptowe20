import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RequestService {

  constructor(private http: HttpClient) { }

  fetchExchangerates(url: string) {
    return this.http.get(url);
  }

  fetchSaleData(url: string) {
    return this.http.get(url);
  }
}
