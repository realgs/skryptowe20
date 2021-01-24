using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using KosmaKotschmarówLab7ZadanieDomowe.Models;
using Newtonsoft.Json;

namespace KosmaKotschmarówLab7ZadanieDomowe.services
{
    public class DataSource
    {

        HttpClient client = new HttpClient();
        
        public async Task<CurrencyModel> GetCurrencyAsync(string currencyCode, DateTime date)
        {
            string path = "http://api.nbp.pl/api/exchangerates/rates/" + string.Format("{0}/{1}/{2}", "A", currencyCode, date.ToString("yyyy-MM-dd"));
            CurrencyModel currency = null;
            HttpResponseMessage response = await client.GetAsync(path);
            if (response.IsSuccessStatusCode)
            {
                var jsonString = await response.Content.ReadAsStringAsync();
                currency = JsonConvert.DeserializeObject<CurrencyModel>(jsonString);
            }
            return currency;
        }
    }
}
