import React from 'react';
import { withRouter } from 'react-router-dom';
import { useLocation } from "react-router-dom";
import { useHistory } from "react-router-dom";
import LineChart from './components/LineChart';



function DataTable(){

	const location = useLocation();
	const history = useHistory();

	var type = location.type;
	var date = location.date;
	var startDate = location.startDate;
	var endDate = location.endDate;
	var json = location.json;

	const ObjectToArray = (object) => {
		var array = []
		for (var key in object) {
			if (object.hasOwnProperty(key)) {
				array.push(object[key]);
			}
		}
		return array;
	}

	const goToResult = () => {
		let path = '/';
		history.push(path);
	}

	const PrepareTable = () => {
		if (type == "exchangeRates") {
			var array = ObjectToArray(json);
			if (array[0].date != null) {
				return array.map(item => (
					<li key={item.id}>
						Date: {item.date} | Interpolated: {item.interpolated.toString()} | USD to PLN: {item.usd_to_pln}
					</li>
				))
			}
			else {
				return <div style={{ color: "red" }}>{json.toString()}</div>
			}
		}
		else if (type == "rangeSales" || type == "specificSales") {
			if (json.COUNT != null) {
				return <div><li> Count: {json.COUNT}</li >
					<li>Sum in PLN: {json.SUM_IN_PLN} </li>
					<li>Sum in USD: {json.SUM_IN_USD} </li></div>
			}
			else{
				return <div style={{ color: "red" }}>{json.toString()}</div>
			}
		}
	}

	const ShowGraphIfEgible = () => {
		if (type == "exchangeRates"){
			return <LineChart />
		}
	}

	return (
		<div className="App-body">
			<button onClick={goToResult}>RETURN</button>
			<h1 className="App-header">{date}</h1>
			<h1 className="App-header">{startDate} - {endDate}</h1>
			<table className="App-text">
				<tr>
					<td>
						<ul>
							{console.log(ObjectToArray(json))}
							{PrepareTable()}
						</ul>
					</td>
					<td width="100"/>
					<td className="App-chart">
						{ShowGraphIfEgible()}
					</td>
				</tr>
			</table>
		</div>
	)
}

export default withRouter(DataTable);