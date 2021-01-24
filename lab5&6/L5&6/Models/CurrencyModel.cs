using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace KosmaKotschmarówLab7ZadanieDomowe.Models
{
    public class CurrencyModel
    {
        /// <summary>
        /// typ tabeli
        /// </summary>
        public string Table { get; set; }
        /// <summary>
        /// nazwa waluty
        /// </summary>
        public string Currency { get; set; }
        /// <summary>
        /// kod waluty
        /// </summary>
        public string Code { get; set; }
        /// <summary>
        /// lista kursów poszczególnych walut w tabeli
        /// </summary>
        public RateModel[] Rates { get; set; }
    }

    public class RateModel
    {
        /// <summary>
        /// numer tabeli
        /// </summary>
        public string No { get; set; }
        /// <summary>
        /// data publikacji
        /// </summary>
        public string EffectiveDate { get; set; }
        /// <summary>
        /// przeliczony kurs średni waluty 
        /// </summary>
        public float Mid { get; set; }
    }

}
