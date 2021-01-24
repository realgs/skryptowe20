using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using KosmaKotschmarówLab7ZadanieDomowe.Models;

namespace KosmaKotschmarówLab7ZadanieDomowe.services
{
    public interface ICurrencyService
    {

        CurrencyModel GetRate(string currency, DateTime date);
        List<CurrencyModel> GetRates(string currency, DateTime startDate, DateTime endDate);
    }
}
