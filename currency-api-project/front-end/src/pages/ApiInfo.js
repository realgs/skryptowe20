import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

function createData(name, type, desc) {
    return { name, type, desc };
}

function createDataResp(code, desc) {
    return { code, desc };
}

const rows_model_1 = [
    createData('date', 'datetime RRRR-MM-DD', 'Data dla której zwracany jest kurs'),
    createData('rate', 'float', 'Kurs PLN-USD'),
    createData('interpolated', 'bool', 'Czy wartość została przeniesiona z poprzedniego dnia z powodu braku danych')
];

const rows_responses_1 = [
    createDataResp('200', 'Zwraca listę rate_dto'),
    createDataResp('400', 'Dla niepoprawnie sformatowanych dat'),
    createDataResp('400', 'Jeśli pojawią się dni spoza zakresu')
];

const rows_model_2 = [
    createData('date', 'datetime RRRR-MM-DD', 'Data dla której zwracane są wyniki'),
    createData('profit_usd', 'float', 'Dochód z danego dnia w USD'),
    createData('profit_pln', 'float', 'Dochód z danego dnia w PLN')
];

const rows_responses_2 = [
    createDataResp('200', 'Zwraca listę profit_dto'),
    createDataResp('400', 'Dla niepoprawnie sformatowanych dat'),
    createDataResp('400', 'Jeśli pojawią się dni spoza zakresu')
];

const useStyles = makeStyles({
    table: {
      minWidth: 100,
    },
});

export default function Income() 
{
    const classes = useStyles();

    return (
        <div style={{background: 'grey', textAlign: 'left', height:'100%'}}>
            <div style={{marginLeft: '50px'}}>
                <h2>API walutowe: lista 5 języki skryptowe</h2>
                <br/>
                <h3>Endpointy:</h3>
                <div style={{marginLeft: '20px'}}>
                <br/>
                    <a href='rates' style={{color: 'black'}}><h5>{"GET /rates/from/<date_from>/to/<date_to>"}</h5></a>
                    {"Gdzie <date_from> i <date_to> to daty w formacie RRRR-MM-DD"}
                    <div style={{marginLeft: '20px'}}>
                        <br/><h6>Model rate_dto:</h6>
                        <TableContainer component={Paper} style={{width: '900px'}}>
                            <Table className={classes.table} aria-label="simple table">
                                <TableHead>
                                <TableRow>
                                    <TableCell>Nazwa</TableCell>
                                    <TableCell>Typ danych</TableCell>
                                    <TableCell>Opis</TableCell>
                                </TableRow>
                                </TableHead>
                                <TableBody>
                                {rows_model_1.map((row) => (
                                    <TableRow key={row.name}>
                                    <TableCell component="th" scope="row">{row.name}</TableCell>
                                    <TableCell align="left">{row.type}</TableCell>
                                    <TableCell align="left">{row.desc}</TableCell>
                                    </TableRow>
                                ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    </div>

                    <div style={{marginLeft: '20px'}}>
                        <br/><h6>Odpowiedzi:</h6>
                        <TableContainer component={Paper} style={{width: '900px'}}>
                            <Table className={classes.table} aria-label="simple table">
                                <TableHead>
                                <TableRow>
                                    <TableCell>Kod</TableCell>
                                    <TableCell align="left">Opis</TableCell>
                                </TableRow>
                                </TableHead>
                                <TableBody>
                                {rows_responses_1.map((row) => (
                                    <TableRow key={row.code}>
                                    <TableCell component="th" scope="row">{row.code}</TableCell>
                                    <TableCell align="left">{row.desc}</TableCell>
                                    </TableRow>
                                ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    </div>
                </div>

                <div style={{marginLeft: '20px'}}>
                <br/>
                    <a href='income' style={{color: 'black'}}><h5>{"GET /profits/day/<date_from>/to/<date_to>"}</h5></a>
                    {"Gdzie <date_from> i <date_to> to daty w formacie RRRR-MM-DD"}
                    <div style={{marginLeft: '20px'}}>
                        <br/><h6>Model profit_dto:</h6>
                        <TableContainer component={Paper} style={{width: '900px'}}>
                            <Table className={classes.table} aria-label="simple table">
                                <TableHead>
                                <TableRow>
                                    <TableCell>Nazwa</TableCell>
                                    <TableCell align="left">Typ danych</TableCell>
                                    <TableCell align="left">Opis</TableCell>
                                </TableRow>
                                </TableHead>
                                <TableBody>
                                {rows_model_2.map((row) => (
                                    <TableRow key={row.name}>
                                    <TableCell component="th" scope="row">{row.name}</TableCell>
                                    <TableCell align="left">{row.type}</TableCell>
                                    <TableCell align="left">{row.desc}</TableCell>
                                    </TableRow>
                                ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    </div>

                    <div style={{marginLeft: '20px'}}>
                        <br/><h6>Odpowiedzi:</h6>
                        <TableContainer component={Paper} style={{width: '900px'}}>
                            <Table className={classes.table} aria-label="simple table">
                                <TableHead>
                                <TableRow>
                                    <TableCell>Kod</TableCell>
                                    <TableCell align="left">Opis</TableCell>
                                </TableRow>
                                </TableHead>
                                <TableBody>
                                {rows_responses_2.map((row) => (
                                    <TableRow key={row.code}>
                                    <TableCell component="th" scope="row">{row.code}</TableCell>
                                    <TableCell align="left">{row.desc}</TableCell>
                                    </TableRow>
                                ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    </div>
                </div>
            </div>
        </div>
    )
}
