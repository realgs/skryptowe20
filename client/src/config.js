import ENV from '@/env';

const config = {};

if (ENV === 'dev') {
  config.apiPath = 'http://127.0.0.1:5000';
} else {
  config.apiPath = '';
}

config.codes = ['THB', 'USD', 'AUD', 'HKD', 'CAD', 'NZD', 'SGD', 'EUR', 'HUF', 'CHF', 'GBP', 'UAH',
  'JPY', 'CZK', 'DKK', 'ISK', 'NOK', 'SEK', 'HRK', 'RON', 'BGN', 'TRY', 'ILS', 'CLP', 'PHP',
  'MXN', 'ZAR', 'BRL', 'MYR', 'RUB', 'IDR', 'INR', 'KRW', 'CNY', 'XDR', 'AFN', 'MGA', 'PAB',
  'ETB', 'VES', 'BOB', 'CRC', 'SVC', 'NIO', 'GMD', 'MKD', 'DZD', 'BHD', 'IQD', 'JOD', 'KWD',
  'LYD', 'RSD', 'TND', 'MAD', 'AED', 'STN', 'BSD', 'BBD', 'BZD', 'BND', 'FJD', 'GYD', 'JMD',
  'LRD', 'NAD', 'SRD', 'TTD', 'XCD', 'SBD', 'ZWL', 'VND', 'AMD', 'CVE', 'AWG', 'BIF', 'XOF',
  'XAF', 'XPF', 'DJF', 'GNF', 'KMF', 'CDF', 'RWF', 'EGP', 'GIP', 'LBP', 'SSP', 'SDG', 'SYP',
  'GHS', 'HTG', 'PYG', 'ANG', 'PGK', 'LAK', 'MWK', 'ZMW', 'AOA', 'MMK', 'GEL', 'MDL', 'ALL',
  'HNL', 'SLL', 'SZL', 'LSL', 'AZN', 'MZN', 'NGN', 'ERN', 'TWD', 'TMT', 'MRU', 'TOP', 'MOP',
  'ARS', 'DOP', 'COP', 'CUP', 'UYU', 'BWP', 'GTQ', 'IRR', 'YER', 'QAR', 'OMR', 'SAR', 'KHR',
  'BYN', 'LKR', 'MVR', 'MUR', 'NPR', 'PKR', 'SCR', 'PEN', 'KGS', 'TJS', 'UZS', 'KES', 'SOS',
  'TZS', 'UGX', 'BDT', 'WST', 'KZT', 'MNT', 'VUV', 'BAM'];

export default config;
