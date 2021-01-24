using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using KosmaKotschmarówLab7ZadanieDomowe.Models;
using KosmaKotschmarówLab7ZadanieDomowe.services;
using Microsoft.AspNetCore.Mvc;

namespace KosmaKotschmarówLab7ZadanieDomowe.Controllers
{
    [Route("[controller]")]
    public class ApiController : Controller
    {
        private ICurrencyService _currencyService;

        public ApiController(ICurrencyService currencyService)
        {
            _currencyService = currencyService;
        }

        public ActionResult Index()
        {
            List<SimpleCurrencyModel> currencies = new List<SimpleCurrencyModel>();
            currencies.Add(new SimpleCurrencyModel("dolar amerykański", "USD", _currencyService.GetRate("USD", DateTime.Today).Rates[0].Mid));
            currencies.Add(new SimpleCurrencyModel("funt szterling", "GBP", _currencyService.GetRate("USD", DateTime.Today).Rates[0].Mid));
            currencies.Add(new SimpleCurrencyModel("korona czeska", "CZK", _currencyService.GetRate("USD", DateTime.Today).Rates[0].Mid));
   
         
            return View(currencies);// addded parameter
        }

        public ActionResult Details(int id)
        {


            return View(); // added parameter
        }
    }
}
