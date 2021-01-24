using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using KosmaKotschmarówLab7ZadanieDomowe.Models;
using KosmaKotschmarówLab7ZadanieDomowe.services;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace KosmaKotschmarówLab7ZadanieDomowe.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CurrencyController : Controller
    {
        private ICurrencyService _currencyService;

        /// <summary>
        /// konstruktor przyjmujący currencyService
        /// </summary>
        /// <param name="currencyService"></param>
        public CurrencyController(ICurrencyService currencyService)
        {
            _currencyService = currencyService;
        }

        // GET: CurrencyController
        public ActionResult Index()
        {
            return View();
        }

        [HttpGet]
        public IActionResult Get()
        {
            var rate = _currencyService.GetRate("USD", DateTime.Today);
            return Ok(rate);
        }

        [HttpGet]
        [Route("{currency}")]
        public IActionResult Get([FromRoute]string currency)
        {
            var rate = _currencyService.GetRate(currency, DateTime.Today);
            return Ok(rate);
        }

        [HttpGet]
        [Route("{currency}/{date}")]
        public IActionResult Get([FromRoute] string currency, [FromRoute] string date)
        {
            DateTime dateToUse;
            DateTime.TryParse(date, out dateToUse);
            var rate = _currencyService.GetRate(currency, dateToUse);
            return Ok(rate);
        }
        [HttpGet]
        [Route("{currency}/{startDate}/{endDate}")]
        public IActionResult Get(string currency, string startDate, string endDate)
        {
            DateTime startDateToUse, endDateToUse;
            DateTime.TryParse(startDate, out startDateToUse);
            DateTime.TryParse(endDate, out endDateToUse);

            List<CurrencyModel> ratesList = _currencyService.GetRates(currency, startDateToUse, endDateToUse);
            return Ok(ratesList);
        }

    }
}
