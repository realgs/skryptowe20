import React, { useEffect, useState } from "react";
import { Typography, Container, Grid, Box, MenuItem, TextField, Button } from "@material-ui/core";
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';
import { Bar } from 'react-chartjs-2'
import blue from '@material-ui/core/colors/blue';

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
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(5);
    const [symbol, setSymbol] = useState('PLN');
    const [startDate, setStartDate] = useState('2004-01-01');
    const [endDate, setEndDate] = useState('2005-01-01');

    const chartData = {
        labels: data.map(row => row.date),
        datasets: [
            {
                label: 'Sales',
                data: data.map(row => row.sales_sum),
                fill: false,
                borderColor: blue[500],
                backgroundColor: blue[500],
            }
        ]
    }

    const columns = [
        { id: 'date', label: 'Date' },
        { id: 'sales_sum', label: 'Sales Sum' },
    ];

    const url = `http://127.0.0.1:8000/api/sales/?symbol=${symbol}&start=${startDate}&end=${endDate}`

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

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(+event.target.value);
        setPage(0);
    };

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
                                Sales API
                        </Typography>
                            <hr />
                            <Grid container direction="row" justify="space-evenly" alignItems="center">
                                <TextField
                                    label="Currency"
                                    id="symbolSelect"
                                    defaultValue="USD"
                                    value={symbol}
                                    onChange={handleChangeSymbol}
                                    select>
                                    <MenuItem value="PLN">PLN</MenuItem>
                                    <MenuItem value="USD">USD</MenuItem>
                                    <MenuItem value="EUR">EUR</MenuItem>
                                    <MenuItem value="CHF">CHF</MenuItem>
                                </TextField>
                                <TextField
                                    className={`${(new Date(startDate) < new Date("2003-01-06")) ? classes.textField : ''}`}
                                    color={`${(new Date(startDate) < new Date("2003-01-06")) ? 'secondary' : 'primary'}`}
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
                                    disabled={(new Date(startDate) < new Date('2003-01-06')) || (new Date(endDate) < new Date(startDate))}
                                    onClick={() => { loadData(url); }}>Refresh</Button>
                            </Grid>
                            <hr />
                        </Container>
                    </form>

                    <Box display="flex" flexWrap="wrap" alignItems="center">
                        <Container maxWidth="sm">
                            <Paper>
                                <TableContainer>
                                    <Table stickyHeader aria-label="sticky table">
                                        <TableHead>
                                            <TableRow>
                                                {columns.map((column) => (
                                                    <TableCell key={column.id} align="left">
                                                        {column.label}
                                                    </TableCell>
                                                ))}
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {data.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row) => {
                                                return (
                                                    <TableRow hover role="checkbox" tabIndex={-1} key={data.date}>
                                                        {columns.map((column) => {
                                                            const value = row[column.id];
                                                            return (
                                                                <TableCell key={column.id} align="left">
                                                                    {String(value).toUpperCase()}
                                                                </TableCell>
                                                            );
                                                        })}
                                                    </TableRow>
                                                );
                                            })}
                                        </TableBody>
                                    </Table>
                                </TableContainer>
                                <TablePagination
                                    rowsPerPageOptions={[5, 10, 25, 100]}
                                    component="div"
                                    count={data.length}
                                    rowsPerPage={rowsPerPage}
                                    page={page}
                                    onChangePage={handleChangePage}
                                    onChangeRowsPerPage={handleChangeRowsPerPage}
                                />
                            </Paper>
                        </Container>
                        <Container maxWidth="md">
                            <Paper>
                                <Bar data={chartData} />
                            </Paper>
                        </Container>
                    </Box>
                </div>

            </main>


        </React.Fragment>

    );

}


export default Currency;
