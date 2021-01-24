using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace KosmaKotschmarówLab7ZadanieDomowe.Models
{
    public class SimpleCurrencyModel
    {
        /// <summary>
        /// pełna nazwa
        /// </summary>
        public string Currency { get; set; }
        /// <summary>
        /// kod waludty
        /// </summary>
        public string Code { get; set; }
        /// <summary>
        /// przeliczony kurs średni waluty 
        /// </summary>
        public float Mid { get; set; }

        public SimpleCurrencyModel(string currency, string code, float mid)
        {
            Currency = currency;
            Code = code;
            Mid = mid;
        }
    }
}
