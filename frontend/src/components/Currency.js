import React, { useEffect, useState } from "react";
import { Typography, Container, Grid, Box, MenuItem, TextField, Button } from "@material-ui/core";
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import { Line } from 'react-chartjs-2';
import blue from '@material-ui/core/colors/blue';
import TableData from './TableData';


const useStyles = makeStyles(theme => ({
    heroContent: {
        backgroundColor: theme.palette.background.paper,
        padding: theme.spacing(8, 0, 6),
    },
    textField: {
        "& .MuiFormLabel-root": {
            color: "red",
        },
        "& .MuiInput-underline::before": {
            borderColor: "red",
        },
    }

}));


const Currency = () => {
    const [data, setData] = useState([]);
    const [symbol, setSymbol] = useState('USD');
    const [startDate, setStartDate] = useState('2020-01-01');
    const [endDate, setEndDate] = useState('2020-01-11');

    const chartData = {
        labels: data.map(row => row.date),
        datasets: [
            {
                label: 'Currency',
                data: data.map(row => row.value),
                fill: false,
                borderColor: blue[500],
            }
        ]
    }

    const columns = [
        { id: 'date', label: 'Date' },
        { id: 'value', label: 'Value' },
        { id: 'interpolated', label: 'Interpolated' },
    ];

    const url = `http://127.0.0.1:8000/api/currency/?symbol=${symbol}&start=${startDate}&end=${endDate}`

    useEffect(() => {
        loadData(url);
    }, []);

    const loadData = async (url) => {
        const response = await fetch(url, {
            method: 'GET',
            mode: 'cors',
            credentials: 'same-origin',
            headers: new Headers({
                'Authorization': 'Token 30ab088341086f247cfdf93375725a2c910b9cb5',
                'Content-Type': 'application/json'
            })
        });
        const data = await response.json()
        setData(data);
    }

    const handleChangeSymbol = (event) => {
        setSymbol(event.target.value);
    }

    const handleChangeStartDate = (event) => {
        setStartDate(event.target.value);
    }

    const handleChangeEndDate = (event) => {
        setEndDate(event.target.value);
    }

    const classes = useStyles()

    return (
        <React.Fragment>
            <main>
                <div className={classes.heroContent}>
                    <form noValidate>
                        <Container maxWidth="lg">
                            <Typography variant="h2" component="h1" align="center" color="textPrimary">
                                Currency API
                        </Typography>
                            <hr />
                            <Grid container direction="row" justify="space-evenly" alignItems="center">
                                <TextField
                                    label="Currency"
                                    id="symbolSelect"
                                    defaultValue="USD"
                                    value={symbol}
                                    onChange={handleChangeSymbol}
                                    color="secondary"
                                    select>
                                    <MenuItem value="USD">USD</MenuItem>
                                    <MenuItem value="EUR">EUR</MenuItem>
                                    <MenuItem value="CHF">CHF</MenuItem>
                                </TextField>
                                <TextField
                                    className={`${(new Date(startDate) < new Date("2002-01-02")) ? classes.textField : ''}`}
                                    color={`${(new Date(startDate) < new Date("2002-01-02")) ? 'secondary' : 'primary'}`}
                                    id="startDate"
                                    label="Start date"
                                    type="date"
                                    value={startDate}
                                    onChange={handleChangeStartDate}
                                    InputLabelProps={{
                                        shrink: true,
                                    }}
                                />
                                <TextField
                                    className={`${(new Date(endDate) < new Date(startDate)) ? classes.textField : ''}`}
                                    color={`${(new Date(endDate) < new Date(startDate)) ? 'secondary' : 'primary'}`}
                                    id="endDate"
                                    label="End date"
                                    type="date"
                                    defaultValue={endDate}
                                    value={endDate}
                                    onChange={handleChangeEndDate}
                                    InputLabelProps={{
                                        shrink: true,
                                    }}
                                />
                                <Button
                                    disabled={(new Date(startDate) < new Date('2002-01-02')) || (new Date(endDate) < new Date(startDate))}
                                    onClick={() => { loadData(url); }}>Refresh</Button>
                            </Grid>
                            <hr />
                        </Container>
                    </form>

                    <Box display="flex" flexWrap="wrap" alignItems="center">
                        <TableData data={data} columns={columns} />
                        <Container maxWidth="md">
                            <Paper>
                                <Line data={chartData} />
                            </Paper>
                        </Container>
                    </Box>
                </div>
            </main>


        </React.Fragment>

    );

}


export default Currency;
