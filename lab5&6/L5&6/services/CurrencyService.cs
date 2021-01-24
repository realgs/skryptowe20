using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Threading.Tasks;
using KosmaKotschmarówLab7ZadanieDomowe.Models;

namespace KosmaKotschmarówLab7ZadanieDomowe.services
{
    public class CurrencyService : ICurrencyService
    {
        DataSource currencyDataSource = new DataSource();

        public CurrencyModel GetRate(string currency, DateTime date)
        {
            var result = currencyDataSource.GetCurrencyAsync(currency, date).Result;
            while (result == null)
            {
                date = date.AddDays(-1);
                result = currencyDataSource.GetCurrencyAsync(currency, date).Result;
            }
            return result;
        }

        public List<CurrencyModel> GetRates(string currency, DateTime startDate, DateTime endDate)
        {
            List<CurrencyModel> ratesList = new List<CurrencyModel>();
            
            while(startDate <= endDate)
            {              
                ratesList.Add(GetRate(currency, startDate));
                startDate = startDate.AddDays(1);
            }
            return ratesList;
        }

        /*public DataTable ChartData(string code, DateTime startDate, DateTime endDate)
        {
            DataTable data = new DataTable()
            {

            }

        }*/
    }
}
