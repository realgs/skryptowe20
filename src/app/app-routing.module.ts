import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ExchangeRatesComponent } from './exchange-rates/exchange-rates.component';
import { ReadmeComponent } from './readme/readme.component';
import { SalesComponent } from './sales/sales.component';

const routes: Routes = [
  {path: 'main', component: ReadmeComponent},
  {path: 'sales', component: SalesComponent},
  {path: 'exchangerates', component: ExchangeRatesComponent},


];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
