import React from 'react';
import './App.css';
import { useHistory } from "react-router-dom";
import { withRouter } from 'react-router-dom';

function Home(){

	const history = useHistory();
	
	const goToResultSalesSpecific = () => {
		let path = '/result';
		if (date != null) {
			let [year, month, day] = date.split("-");
			year = year.slice(-2);
			fetch('http://127.0.0.1:5000/api/v1/resources/salessummary?date=' + day + '/' + month + '/' + year)
				.then(res => res.json())
				.then(json => history.push({
					pathname: path,
					json: json,
					type: "specificSales",
					date: date
				}));
		}
		else {
			fetch('http://127.0.0.1:5000/api/v1/resources/salessummary')
				.then(res => res.json())
				.then(json => history.push({
					pathname: path,
					json: json,
					type: "specificSales",
				}));
		}
	}

	const goToResultSalesRange = () => {
		let path = '/result';
		var json = [];
		var data = [];
		if (startDate1 != null) {
			let [year1, month1, day1] = startDate1.split("-");
			year1 = year1.slice(-2);
			if (endDate1 != null) {
				let [year2, month2, day2] = endDate1.split("-");
				year2 = year2.slice(-2);
				fetch('http://127.0.0.1:5000/api/v1/resources/salessummary/range?startdate=' + day1 + '/' + month1 + '/' + year1
					+ '&enddate=' + day2 + '/' + month2 + '/' + year2)
					.then(res => res.json())
					.then(json => history.push({
						pathname: path,
						json: json,
						type: "rangeSales",
						startDate: startDate1,
						endDate: endDate1,
					}));
			}
			else {
				fetch('http://127.0.0.1:5000/api/v1/resources/salessummary/range?startdate=' + day1 + '/' + month1 + '/' + year1)
					.then(res => res.json())
					.then(json => history.push({
						pathname: path,
						json: json,
						type: "rangeSales",
						startDate: startDate1,
						endDate: maxDate,
					}));
			}
		}
		else if (endDate1 != null) {
			let [year2, month2, day2] = endDate1.split("-");
			year2 = year2.slice(-2);
			fetch('http://127.0.0.1:5000/api/v1/resources/salessummary/range?enddate=' + day2 + '/' + month2 + '/' + year2)
				.then(res => res.json())
				.then(json => history.push({
					pathname: path,
					json: json,
					type: "rangeSales",
					startDate: minDate,
					endDate: endDate1,
				}));
		}
		else {
				fetch('http://127.0.0.1:5000/api/v1/resources/salessummary/range')
					.then(res => res.json())
					.then(json => history.push({
						pathname: path,
						json: json,
						type: "rangeSales",
						startDate: minDate,
						endDate: maxDate,
					}));
		}
	}

	const goToResultExchangeRates = () => {
		let path = '/result';
		if (startDate2 != null) {
			let [year1, month1, day1] = startDate2.split("-");
			year1 = year1.slice(-2);
			if (endDate2 != null) {
				let [year2, month2, day2] = endDate2.split("-");
				year2 = year2.slice(-2);
				fetch('http://127.0.0.1:5000/api/v1/resources/exchangerates?startdate=' + day1 + '/' + month1 + '/' + year1
					+ '&enddate=' + day2 + '/' + month2 + '/' + year2)
					.then(res => res.json())
					.then(json => history.push({
						pathname: path,
						json: json,
						type: "exchangeRates",
						startDate: startDate2,
						endDate: endDate2,
						data: PrepareGraphDataExchangeRate(json)
					}));
			}
			else {
				fetch('http://127.0.0.1:5000/api/v1/resources/exchangerates?startdate=' + day1 + '/' + month1 + '/' + year1)
					.then(res => res.json())
					.then(json => history.push({
						pathname: path,
						json: json,
						type: "exchangeRates",
						startDate: startDate2,
						endDate: maxDate,
						data: PrepareGraphDataExchangeRate(json)
					}));
			}
		}
		else if (endDate2 != null) {
			let [year2, month2, day2] = endDate2.split("-");
			year2 = year2.slice(-2);
			fetch('http://127.0.0.1:5000/api/v1/resources/exchangerates?enddate=' + day2 + '/' + month2 + '/' + year2)
				.then(res => res.json())
				.then(json => history.push({
					pathname: path,
					json: json,
					type: "exchangeRates",
					startDate: minDate,
					endDate: endDate2,
					data: PrepareGraphDataExchangeRate(json)
				}));
		}
		else {
			fetch('http://127.0.0.1:5000/api/v1/resources/exchangerates')
				.then(res => res.json())
				.then(json => history.push({
					pathname: path,
					json: json,
					type: "exchangeRates",
					startDate: minDate,
					endDate: maxDate,
					data: PrepareGraphDataExchangeRate(json)
				}));
		}
	}

	var date;
	var startDate1;
	var endDate1;
	var startDate2;
	var endDate2;

	const minDate = '2017-08-30';
	const maxDate = '2020-12-11';

	const handleInputChange = (event) => {
		const target = event.target;
		const value = target.value;
		const name = target.name;
		if (name == "date") {
			date = value;
		}
		else if (name == "startDate1") {
			startDate1 = value;
		}
		else if (name == "endDate1") {
			endDate1 = value;
		}
		else if (name == "startDate2") {
			startDate2 = value;
		}
		else if (name == "endDate2") {
			endDate2 = value;
		}
	}

	const PrepareGraphDataExchangeRate = (json) => {
		var labels = [];
		var data = [];
		for (var key in json) {
			if (json.hasOwnProperty(key)) {
				labels.push(json[key].date);
				data.push(json[key].usd_to_pln);
			}
		}
		var dataHolder = {
			labels: labels,
			datasets: [
				{
					label: 'Kurs USD do PLN',
					data: data,
					borderColor: ['rgba(81, 240, 46, 0.8)'],
					backgroundColor: ['rgba(81, 240, 46, 0.2)'],
					pointBackgroundColor: ['rgba(81, 240, 46, 0.2)'],
					pointBorderColor: ['rgba(81, 240, 46, 0.8)']
				}
			]
		}
		return dataHolder;
	}

	const PrepareGraphDataSalesRange = () => {
		var labels = [];
		var dataUSD = [];
		var dataPLN = [];

		var startDate = startDate1;
		if (startDate == null) {
			startDate = minDate;
		}
		var endDate = endDate1;
		if (endDate == null) {
			endDate = maxDate;
		}

		var dates = getDates(startDate, endDate);

		console.log(dates);
		//Api prepared for previous laboratory did not have function for getting list of sales - only summaries.
		//Therefore, until backend programist (in this case me) won't put another function, we have to check every date separetly.
		var i;
		for (i = 0; i < dates.length; i++) {
			var j = i;
			console.log(dates[j]);
			fetch('http://127.0.0.1:5000/api/v1/resources/salessummary?date=' + dates[j].getDate() + '/' + dates[j].getMonth() + '/' + dates[j].getFullYear().toString().slice(-2))
				.then(res => res.json())
				.then(fetchedJson => {
					console.log(fetchedJson);
					var json = fetchedJson;
					console.log(json);
					dataUSD.push(json.SUM_IN_USD);
					dataPLN.push(json.SUM_IN_PLN);
				})
				.then(a => {
					labels.push(dates[j]);
				})
				.then(b => {
					if (j == dates.length - 1) {
						var dataHolder = {
							labels: labels,
							datasets: [
								{
									label: 'Przychód z wypożyczeń w dolarach',
									data: dataUSD,
									borderColor: ['rgba(81, 240, 46, 0.8)'],
									backgroundColor: ['rgba(81, 240, 46, 0.2)'],
									pointBackgroundColor: ['rgba(81, 240, 46, 0.2)'],
									pointBorderColor: ['rgba(81, 240, 46, 0.8)']
								},
								{
									label: 'Przychód z wypożyczeń w złotówkach',
									data: dataPLN,
									borderColor: ['rgba(224, 58, 29, 0.8)'],
									backgroundColor: ['rgba(224, 58, 29, 0.2)'],
									pointBackgroundColor: ['rgba(224, 58, 29, 0.2)'],
									pointBorderColor: ['rgba(224, 58, 29, 0.8)']
								}
							]
						}

						console.log(dataHolder);

						return dataHolder;
					}
					else {
						console.log(j + " / " + dates.length);
					}
				});
		}
	}

	const getDates = (startDate, stopDate) => {
		var dateArray = new Array();
		var currentDate = new Date(startDate);
		var endDate = new Date(stopDate);
		var days = currentDate.getDate();
		console.log(currentDate);
		console.log(endDate);
		console.log(currentDate <= stopDate)
		while (currentDate <= endDate) {
			dateArray.push(new Date(currentDate));
			currentDate.setDate(++days);
			days = currentDate.getDate();
		}
		return dateArray;
	}

	return(
	<div className="App">
		<head className="App-header">
			<h1>
				DVD RENTAL API
			</h1>		    
        </head>
	    <body className="App-body">
			<div className="App-space">&nbsp;</div>
			<h2 className="App-header">Wyszukiwanie sprzedaży</h2>
			<div>
				<h3 className="App-text">Sprzedaż w wybranym dniu:</h3>
					<table className="App-table">
						<tr><td>Dzień sprzedaży:&nbsp;</td><td><input type="date" name="date" onChange={handleInputChange} /></td></tr>
					<tr><td/><td width="115"><button type="button" onClick={goToResultSalesSpecific}>Zobacz wyniki</button></td></tr>
				</table>
				<h3 className="App-text">Sprzedaż w przedziale dni:</h3>
				<table className="App-table">
						<tr><td width="5">Od:&nbsp;</td><td><input type="date" name="startDate1" onChange={handleInputChange} /></td><td width="50">Do:&nbsp;</td><td><input type="date" name="endDate1" onChange={handleInputChange}/></td></tr>
						<tr><td /><td /><td /><td><button type="button" onClick={goToResultSalesRange}>Zobacz wyniki</button></td></tr>
				</table>
				<br/>
			<h2 className="App-header">Przeglądanie kursów walut</h2>
				<h3 className="App-text">Kursy w przedziale dni:</h3>
				<table className="App-table">
						<tr><td width="50">Od:&nbsp;</td><td><input type="date" name="startDate2" onChange={handleInputChange} /></td><td width="50">Do:&nbsp;</td><td><input type="date" name="endDate2" onChange={handleInputChange} /></td></tr>
						<tr><td /><td /><td /><td><button type="button" onClick={goToResultExchangeRates}>Zobacz wyniki</button></td></tr>
				</table>
				<br/>
			</div>
			<h2 className="App-header">Wstęp</h2>
			<p className="App-text">
				Niniejsze API umożliwia użytkownikowi sprawdzenie podsumowania transakcji z wybranego okresu, podliczając zyski w dwóch walutach, oraz sprawdzenie użytych do liczenia zysków kursów USD z danych okresów.
				<br/>
				<br/>
				Komunikacja z serwisem polega na wysłaniu odpowiednio sparametryzowanego żądania HTTP GET pod adres:&nbsp;
				<a
					className="App-link"
					href="http://127.0.0.1:5000/"
				>
				http://127.0.0.1:5000/
				</a>
				.
				<br/>
				<br/>
				Do korzystania z API wymagane jest połączenie z bazą danych dvdrental,
				przechowywaną lokalnie na maszynie należącej do wypożyczalni pod adresem&nbsp;
				<a
					className="App-link"
					href="http://127.0.0.1:5000/"
				>
				postgres://postgres:bazman@localhost:5432/dvdrental
				</a>
				<br/>
			</p>
			<h2 className="App-header">Instalacja zależności</h2>
			<p className="App-text">
				Wszystkie zależności można znaleźć w specjalnie przygotowanym pliku 
				<b> requirements.txt</b>.
				<br/>
				Instalacje można uprościć do wywołania komendy <i>pip install -r requirements.txt</i>.
			</p>
			<h2 className="App-header">Instrukcja użytkowania</h2>
			<p className="App-text">
				<h3>Informacje ogólne</h3>
				<ul className="App-text">
					<li>Odpowiedź serwisu zwracana jest w formacie json.</li>
					<li>Dane archiwalne dotyczące kursów USD i podsumowań transakcji dostępne są w przedziale czasu od <b>2017-08-30</b> do <b>2020-12-11</b>, kiedy to sklep zawiesił działalność, wygryziony z rynku przez serwisy streamingowe. Właściciel sklepu zaznacza sobie jednak możliwość edycji tych dat, w razie gdyby
					działalność wypożyczalni została wznowiona.</li>
				</ul>
				<h3>Opis funkcji API dotyczącej kursów</h3>
				<p>
					Funkcja pobierająca kursy USD w stosunku do PLN znajduje się pod adresem:
					<br/>
					<a
						className="App-link"
						href="http://127.0.0.1:5000/api/v1/resources/exchangerates"
					>
						http://127.0.0.1:5000/api/v1/resources/exchangerates
					</a>
					<br/>
					<br/>
					Przyjmuje następujące atrybuty opcjonalne:
					<ul>
					<li>startdate - określa początek zakresu wyszukiwania. Domyślnie ustawiony jest na najwcześniejszą datę w bazie. Format DD/MM/RR. </li>
					<li>enddate - określa koniec zakresu wyszukiwania. Domyślnie ustawiony jest na najpóźniejszą datę w bazie. Format DD/MM/RR. </li>
					</ul>
					<br/>
					Przykłady:
					<ul>
					<li>Pobranie wszystkich kursów w bazie:&nbsp;
						<a
							className="App-link"
							href="http://127.0.0.1:5000/api/v1/resources/exchangerates"
						>
							http://127.0.0.1:5000/api/v1/resources/exchangerates
						</a>
					 </li>
					<li>Pobranie wszystkich kursów od 9 września 2018 roku:&nbsp;
						<a
							className="App-link"
							href="http://127.0.0.1:5000/api/v1/resources/exchangerates?startdate=9/9/18"
						>
							http://127.0.0.1:5000/api/v1/resources/exchangerates?startdate=9/9/18
						</a>
					</li>
					<li>Pobranie wszystkich kursów do 9 września 2018 roku:&nbsp;
						<a
							className="App-link"
							href="http://127.0.0.1:5000/api/v1/resources/exchangerates?enddate=9/9/18"
						>
							http://127.0.0.1:5000/api/v1/resources/exchangerates?enddate=9/9/18
						</a>
					</li>
					<li>Pobranie wszystkich kursów między 3 grudnia 2017 roku a 9 grudnia 2017 roku:&nbsp;
						<a
							className="App-link"
							href="http://127.0.0.1:5000/api/v1/resources/exchangerates?startdate=3/12/17&enddate=9/12/17"
						>	
							http://127.0.0.1:5000/api/v1/resources/exchangerates?startdate=3/12/17&enddate=9/12/17
						</a>
					 </li>
					 </ul>
				</p>
				<h3>Opis funkcji API dotyczącej podsumowań transakcji</h3>
				<p>
					Funkcja pobierająca podsumowania transakcji z informacjami o ich ilości i łącznym przychodzie w dwóch walutach. Występuje w dwóch wersjach:
					<ul>
					<li>Zapytanie o transakcje z konkretnego dnia:&nbsp;
					<a
							className="App-link"
							href="http://127.0.0.1:5000/api/v1/resources/salessummary"
						>
						http://127.0.0.1:5000/api/v1/resources/salessummary
					</a>
					</li>
					<li>Zapytanie o transakcje z przedziału dni:
						<a
							className="App-link"
							href="http://127.0.0.1:5000/api/v1/resources/salessummary/range"
						>
							http://127.0.0.1:5000/api/v1/resources/salessummary/range
						</a>
					</li>
					</ul>
					<h4>Zapytanie o konkretny dzień</h4>
					<p>
						Wymaga podania atrybutu <b>date</b>, który wskazuje, o jaki dzień pytamy.<br/>
						Format DD/MM/RR. 
						<br/>
						Przykład - Informacje o transakcjach z 12 grudnia 2018 roku:
						<a
							className="App-link"
							href="http://127.0.0.1:5000/api/v1/resources/salessummary?date=12/12/18"
						>
						http://127.0.0.1:5000/api/v1/resources/salessummary?date=12/12/18
						</a>
					</p>
					<h4>Zapytanie o przedział dni</h4>
					<p>
						Przyjmuje następujące atrybuty opcjonalne:&nbsp;
						<ul>
						<li><b>startdate</b> - określa początek zakresu wyszukiwania. Domyślnie ustawiony jest na najwcześniejszą datę w bazie. Format DD/MM/RR.
						</li>
						<li><b>enddate</b> - określa koniec zakresu wyszukiwania. Domyślnie ustawiony jest na najpóźniejszą datę w bazie. Format DD/MM/RR.
						</li>
						</ul>
						Przykłady:
						<ul>
						<li>Pobranie podsumowania wszystkich transakcji w bazie:&nbsp;
						<a
							className="App-link"
							href="http://127.0.0.1:5000/api/v1/resources/salessummary/range"
						>
						http://127.0.0.1:5000/api/v1/resources/salessummary/range
						</a>
						</li>
						<li>Pobranie podsumowania wszystkich transakcji w bazie od 9 września 2018 roku:
						<a
							className="App-link"
							href="http://127.0.0.1:5000/api/v1/resources/salessummary/range?startdate=9/9/18"
						>
						http://127.0.0.1:5000/api/v1/resources/salessummary/range?startdate=9/9/18
						</a>
						</li>
						<li>Pobranie podsumowania wszystkich transakcji w bazie do 9 września 2018 roku:
						<a
							className="App-link"
							href="http://127.0.0.1:5000/api/v1/resources/salessummary/range?enddate=9/9/18"
						>
						http://127.0.0.1:5000/api/v1/resources/salessummary/range?enddate=9/9/18
						</a>
						</li>
						<li>Pobranie podsumowania wszystkich transakcji w bazie między 3 grudnia 2017 roku a 9 grudnia 2017 roku:
						<a
							className="App-link"
							href="http://127.0.0.1:5000/api/v1/resources/salessummary/range?startdate=3/12/17&enddate=9/12/17"
						>
						http://127.0.0.1:5000/api/v1/resources/salessummary/range?startdate=3/12/17&enddate=9/12/17
						</a>
						</li>
						</ul>
					</p>
				</p>
				<h3>Ograniczenia</h3>
				<ul>
					<li>Pojedyńczy użytkownik nie może zadać więcej niż 60 zapytań na minutę.</li>
					<li>Użytkownik który przekroczy limit musi odczekać aż limity zostaną odświeżone.</li>
				</ul>
				<h3>Komunikaty błędów</h3>
				<ul>
					<li>W przypadku zadania nieprawidłowo sformułowanych zapytań serwis zwraca komunikat 400 Bad Request wraz z wypisanym powodem i podpowiedzią użytkowania.</li>
					<li>W przypadku przekroczenia limitu zapytań na minutę serwis zwraca komunikat 429 Too Many Requests. </li>
				</ul>
			</p>
        </body>
	    <bottom className="App-bottom">
			<p>
				Szkodziński Kacper 244008 - Języki Skryptowe
			</p>
			<a
			className="App-link"
			href="https://reactjs.org"
			target="_blank"
			rel="noopener noreferrer"
			>
				Learn React
			</a>
	    </bottom>
    </div>
	)
}

export default withRouter(Home);