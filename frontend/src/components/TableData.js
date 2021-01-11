import React, { useState } from "react";
import { Container } from "@material-ui/core";
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';


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


const TableData = (props) => {
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(5);

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(+event.target.value);
        setPage(0);
    };

    const classes = useStyles()

    return (
        <React.Fragment>
            <Container maxWidth="sm">
                <Paper>
                    <TableContainer>
                        <Table stickyHeader aria-label="sticky table">
                            <TableHead>
                                <TableRow>
                                    {props.columns.map((column) => (
                                        <TableCell key={column.id} align="left">
                                            {column.label}
                                        </TableCell>
                                    ))}
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {props.data.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row) => {
                                    return (
                                        <TableRow hover role="checkbox" tabIndex={-1} key={props.data.date}>
                                            {props.columns.map((column) => {
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
                        count={props.data.length}
                        rowsPerPage={rowsPerPage}
                        page={page}
                        onChangePage={handleChangePage}
                        onChangeRowsPerPage={handleChangeRowsPerPage}
                    />
                </Paper>
            </Container>
        </React.Fragment>
    );
}


export default TableData;
