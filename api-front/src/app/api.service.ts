import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  async getData(url: string) {
    try {
      const response = await this.http.get(url).toPromise();
      return response;
    } catch (err) {
      console.log('Api-service error: ');
      console.log(err);
      throw err;
    }
  }
}
