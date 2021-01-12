// import React, {Component} from 'react';
// import PropTypes from 'prop-types';
// import TableContainer from "@material-ui/core/TableContainer";
// import Table from "@material-ui/core/Table";
// import TableHead from "@material-ui/core/TableHead";
// import TableRow from "@material-ui/core/TableRow";
// import Paper from "@material-ui/core/Paper";
// import TableCell from "@material-ui/core/TableCell";
// import TableBody from "@material-ui/core/TableBody";
// import TableFooter from "@material-ui/core/TableFooter";
// import TablePagination from "@material-ui/core/TablePagination";
// import IconButton from "@material-ui/core/IconButton";
// import {useTheme} from "@material-ui/core/styles";
// import FirstPageIcon from '@material-ui/icons/FirstPage'
// import LastPageIcon from '@material-ui/icons/LastPage'
// import KeyboardArrowRight from '@material-ui/icons/KeyboardArrowRight'
// import KeyboardArrowLeft from '@material-ui/icons/KeyboardArrowLeft'
//
// class CurrencyDataComponent extends Component {
//     state = {
//         page: 0,
//         rowsPerPage: 3
//     }
//
//
//     createData = (date, price, interpolation) => {
//         const interpolationValue = interpolation ? 'true' : 'false';
//         return {date, price, interpolationValue};
//     }
//
//     TablePaginationActions = (props) => {
//         const {count, page, rowsPerPage, onChangePage} = props;
//
//         const handleFirstPageButtonClick = (event) => {
//             onChangePage(event, 0);
//         };
//
//         const handleBackButtonClick = (event) => {
//             onChangePage(event, page - 1);
//         }
//
//         const handleNextButtonClick = (event) => {
//             onChangePage(event, page + 1);
//         }
//
//         const handleLastPageButtonClick = (event) => {
//             onChangePage(event, Max.max(0, Math.ceil(count / rowsPerPage) - 1));
//         }
//
//         return (
//             <div>
//                 <IconButton
//                     onClick={handleFirstPageButtonClick}
//                     disabled={page === 0}
//                     aria-label="First Page"
//                 >
//                     {theme.direction === 'rtl' ? <LastPageIcon/> : <FirstPageIcon/>}
//                 </IconButton>
//                 <IconButton
//                     onClick={handleBackButtonClick}
//                     disabled={page === 0}
//                     aria-label="Previous Page"
//                 >
//                     {theme.direction === 'rtl' ? <KeyboardArrowRight/> : <KeyboardArrowLeft/>}
//                 </IconButton>
//                 <IconButton
//                     onClick={handleNextButtonClick}
//                     disabled={page >= Math.ceil(count / rowsPerPage) - 1}
//                     aria-label="Next Page"
//                 >
//                     {theme.direction === 'rtl' ? <KeyboardArrowLeft/> : <KeyboardArrowRight/>}
//                 </IconButton>
//                 <IconButton
//                     onClick={handleLastPageButtonClick}
//                     disabled={page => Math.ceil(count / rowsPerPage) - 1}
//                     aria-label="Last Page"
//                 >
//                     {theme.direction === 'rtl' ? <FirstPageIcon/> : <LastPageIcon/>}
//                 </IconButton>
//             </div>
//         );
//     }
//
//     /* this.TablePaginationActions.propTypes = {
//          count: PropTypes.number.isRequired,
//          onChangePage: PropTypes.func.isRequired,
//          page: PropTypes.number.isRequired,
//          rowsPerPage: PropTypes.number.isRequired
//      }*/
//
//     handleChangePage = (event, newPage) => {
//         this.setState({page: newPage});
//     }
//
//     handleChangeRowsPerPage = (event) => {
//         this.setState({
//             rowsPerPage: parseInt(event.target.value, 10),
//             page: 0
//         });
//     }
//
//     render() {
//         const currencies =
//             this.props.data.map((item) => this.createData(item['date'], item['price'], item['interpolation']));
//         console.log(currencies);
//         return (
//             <TableContainer component={Paper}>
//                 <Table aria-label="simple table">
//                     <TableHead>
//                         <TableRow>
//                             <TableCell>Date</TableCell>
//                             <TableCell>Price</TableCell>
//                             <TableCell>Interpolation</TableCell>
//                         </TableRow>
//                     </TableHead>
//                     <TableBody>
//                         {currencies.map((currency) => (
//                             <TableRow key={currency.date}>
//                                 <TableCell component="th" scope="row">
//                                     {currency.date}
//                                 </TableCell>
//                                 <TableCell>{currency.price}</TableCell>
//                                 <TableCell>{currency.interpolationValue}</TableCell>
//                             </TableRow>
//                         ))}
//                     </TableBody>
//                     <TableFooter>
//                         <TablePagination
//                             rowsPerPageOptions={[3, 5, 10, {label: 'All', value: -1}]}
//                             colSpan={3}
//                             count={currencies.length}
//                             rowsPerPage={this.state.rowsPerPage}
//                             page={this.state.page}
//                             onChangePage={this.state.handleChangePage}
//                             onChangeRowsPerPage={this.state.handleChangeRowsPerPage}
//                             ActionsComponent={this.TablePaginationActions}
//                         />
//                     </TableFooter>
//                 </Table>
//             </TableContainer>
//         );
//     }
// }
//
// export default CurrencyDataComponent;
//
//
// {/*<h1>USD Price for date: {this.props.date}</h1>
//                 <h2>Price: {this.props.price}</h2>
//                 <h2>Interpolation: {this.props.interpolation ? 'true': 'false'}</h2>*/
// }
