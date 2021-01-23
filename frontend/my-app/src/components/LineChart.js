import React from 'react'
import { Line } from 'react-chartjs-2'
import { useLocation } from "react-router-dom";
import { useHistory } from "react-router-dom";

function LineChart() {

    const data2 = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        datasets: [
            {
                label: 'Sales for 2020',
                data: [3, 2, 2, 1, 5],
            }
        ]
    }

    const options = {
        scales: {
            yAxes: [
                {
                    ticks: {
                        min: 3
                    }
                }
            ]
        }
    }

    const location = useLocation();

    var data = location.data;

    return (
        <div>
            <Line data={data} options={options} />
        </div>
    )
}

export default LineChart