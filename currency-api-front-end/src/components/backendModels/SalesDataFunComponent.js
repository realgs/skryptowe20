import React, {Component} from 'react';
import PropTypes from 'prop-types';
import TableContainer from "@material-ui/core/TableContainer";
import Table from "@material-ui/core/Table";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import TableCell from "@material-ui/core/TableCell";
import TableBody from "@material-ui/core/TableBody";
import TableFooter from "@material-ui/core/TableFooter";
import TablePagination from "@material-ui/core/TablePagination";
import {TablePaginationActions} from "./CurrencyDataFunComponent";


function createData(date, plnSalesValue, usdSalesValue) {
    return {date, plnSalesValue, usdSalesValue};
}


TablePaginationActions.propTypes = {
    count: PropTypes.number.isRequired,
    onChangePage: PropTypes.func.isRequired,
    page: PropTypes.number.isRequired,
    rowsPerPage: PropTypes.number.isRequired
};


export default function CustomPaginationSalesTable(props) {
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(3);
    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };


    const sales =
        props.data.map((item) => createData(item['date'], item['pln'], item['usd']));

    return (
        <TableContainer component={Paper}>
            <Table aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell>Date</TableCell>
                        <TableCell>PLN Sales Value</TableCell>
                        <TableCell>USD Sales Value</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {(rowsPerPage > 0
                            ? sales.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                            : sales
                    ).map((sale) => (
                        <TableRow key={sale.date}>
                            <TableCell component="th" scope="row">
                                {sale.date}
                            </TableCell>
                            <TableCell>{sale.plnSalesValue}</TableCell>
                            <TableCell>{sale.usdSalesValue}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
                <TableFooter>
                    <TablePagination
                        rowsPerPageOptions={[3, 5, 10, {label: 'All', value: -1}]}
                        colSpan={3}
                        count={sales.length}
                        rowsPerPage={rowsPerPage}
                        page={page}
                        onChangePage={handleChangePage}
                        onChangeRowsPerPage={handleChangeRowsPerPage}
                        ActionsComponent={TablePaginationActions}
                    />
                </TableFooter>
            </Table>
        </TableContainer>
    );
}

