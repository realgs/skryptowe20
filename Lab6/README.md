## PLN to USD rates, sales data display

This repository contains files needed to run frontend application for data provided by API in: https://github.com/AltiTorie/skryptowe20/tree/Lab5

## Get started
### Install packages

To install and run required packages node and npm is required.
For required packages refer to:
``client/package.json/dependencies``.

## Usage
Go to ./client/ and run in console:
```
npm run serve
```
Go to: **http://localhost:8080**

You can visit 4 subpages:
- /daily_rates - provides PLN to USD rate from selected date 
- /rates - provides PLN to USD rate from range of dates 
- /daily_sales - provides sales data from selected date
- /sales - provides sales data from range of dates

## Project structure

- */client/src/main.js* - main configuration for the application,
- */client/src/App.vue* - main template from which every page is extended,
- */client/src/router/index.js* - contains configuration of routing in this application
- */client/src/components/* - this folder contains Vue components presented in application
- */client/src/assets* - contains additional assets for application
- */client/public/ - contains files shared among the subpages like tab icon
