import * as React from "react";
import { Typography, Container } from "@material-ui/core";
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import grey from '@material-ui/core/colors/grey';

const useStyles = makeStyles((theme) => ({
    heroContent: {
        backgroundColor: theme.palette.background.paper,
        padding: theme.spacing(8, 0, 6),
    },
    links: {
        color: theme.palette.primary.main,
        '&:visited': {
            color: theme.palette.primary.light,
        },
        '&:hover': {
            color: theme.palette.primary.main,
        },
        '&:link': {
            color: theme.palette.primary.light,
        }
    },
    codeSnippet: {
        backgroundColor: grey[700],
        borderRadius: "4px",
        fontStyle: 'mono',
    }
}));


const Snippet = (props) => {
    const classes = useStyles()

    return (
        <a className={classes.codeSnippet}>{props.snippet}</a>
    )
}

const Home = () => {
    const classes = useStyles()

    return (
        <React.Fragment>
            <main>
                <div className={classes.heroContent}>
                    <Container maxWidth="md">
                        <Typography variant="h2" component="h1" align="center" color="textPrimary" >
                            REST with Django Rest Framework
                        </Typography>
                        <Typography variant="h5" align="left" paragraph>
                            <div>
                                This API offers simple GET request, fetching currency values to PLN.
                                It also allows to get sale statistics based date parameter.
                                GET requests return in form of JSON.<br />
                            </div>
                            <br />
                            <ol>
                                <li key="1"><a href="#paragraph1" className={classes.links}>Install Guide</a></li>
                                <li key="2"><a href="#paragraph2" className={classes.links}>Adding new currency</a></li>
                                <li key="3"><a href="#paragraph3" className={classes.links}>API usage</a></li>
                                <li key="4"><a href="#paragraph4" className={classes.links}>Limits</a></li>
                                <li key="5"><a href="#paragraph5" className={classes.links}>Dependencies</a></li>
                                <li key="6"><a href="#paragraph6" className={classes.links}>Credits</a></li>
                            </ol>
                        </Typography>
                        <hr />
                        <Typography id="paragraph1" variant="h4" component="h1" align="center" color="textPrimary" >
                            Install Guide
                        </Typography>
                        <Typography variant="h5" align="left" paragraph>
                            <div>
                                This projects implements automatic database creation for currency values.
                                It also provides sample database file sales.db for sales statistic API demonstration.
                            </div>
                            <br />
                            <ol>
                                <li key="7"><b>Clone this repo:</b><br />

                            <Snippet snippet=" git clone https://github.com/Rochala/skryptowe20.git "/></li>
                                <li key="8"><b>Install requirements</b><br />
                            <Snippet snippet=" pip install -r requirements.txt "/></li>
                                <li key="9"><b>Run initializing script</b><br />
                            <Snippet snippet=" python3 init.py "/></li>
                                <li key="10"><b>Configure Django for your needs</b></li>
                                <li key="11"><b>Start Django server</b><br />
                            <Snippet snippet=" python3 manage.py runserver "/></li>
                            </ol>
                        </Typography>
                        <hr />
                        <Typography id="paragraph2" variant="h4" component="h1" align="center" color="textPrimary" >
                            Adding new currency
                        </Typography>
                        <Typography variant="h5" align="left" paragraph>
                            <ol>
                                <li key="12"><b>Make sure NBP api supports it</b></li>
                                <li key="13"><b>Add new currency symbol to constants.py Currency enum</b></li>
                                <li key="14"><b>Run init.py script to fetch data:</b><br />
                            <Snippet snippet=" python3 init.py "/></li>
                            </ol>
                        </Typography>
                        <hr />
                        <Typography id="paragraph3" variant="h4" component="h1" align="center" color="textPrimary" >
                            API usage
                        </Typography>
                        <Typography variant="h5" align="left" paragraph>
                            <div>
                                Currency data range <Snippet snippet=" http://127.0.0.1:8000/api/currency/?symbol={CURRENCY SYMBOL}start \
                            ={DATE START}&end={DATE END} "/><br /> Example usage for USD between 2020-12-01 and 2020-12-16
                                <Snippet snippet="http://127.0.0.1:8000/api/currency/?symbol=USD&start=2020-12-01&end=2020-12-16 "/>
                            </div>
                            <br />
                            <div>
                                Sales statistics
                               <Snippet snippet=" http://127.0.0.1:8000/api/sales/?start={START DATE}&end={END DATE}&symbol={CURRENCY SYMBOL} "/><br />
                                Example usage for fetching sales from 2005-05-17 to 2006-05-17 in PLN
                                <Snippet snippet=" http://127.0.0.1:8000/api/sales/?start=2005-05-17&end=2006-05-17 "/><br /> You can also get whole
                                range by using <Snippet snippet=" http://127.0.0.1:8000/api/sales/ "/>
                            </div>
                        </Typography>
                        <hr />
                        <Typography id="paragraph4" variant="h4" component="h1" align="center" color="textPrimary" >
                            Limits
                        </Typography>
                        <Typography variant="h5" align="left" paragraph>
                            Minimum sales date = 2003-01-06<br />
                            Minimum currency date = 2002-01-02
                        </Typography>
                        <Table stickyHeader>
                            <TableHead>
                                <TableRow>
                                    <TableCell>User type</TableCell>
                                    <TableCell>Limit</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                <TableRow>
                                    <TableCell align="left">Anonymous user</TableCell>
                                    <TableCell align="left">10 / hour</TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell align="left">Standard user</TableCell>
                                    <TableCell align="left">1000 / hour</TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                        <hr />
                        <Typography id="paragraph5" variant="h4" component="h1" align="center" color="textPrimary" >
                            Dependencies
                        </Typography>
                        <Typography variant="h5" align="left" paragraph>
                            <ul>
                                <li key="16"><a href="https://www.djangoproject.com/" className={classes.links}>Django</a></li>
                                <li key="17"><a href="https://www.django-rest-framework.org/" className={classes.links}>Django REST Framework</a></li>
                                <li key="17"><a href="https://github.com/adamchainz/django-cors-headers" className={classes.links}>Django corsheaders</a></li>
                                <li key="18"><a href="https://github.com/psf/requests" className={classes.links}>requests</a></li>
                                <li key="19"><a href="https://reactjs.org/" className={classes.links}>ReactJS</a></li>
                                <li key="20"><a href="https://material-ui.com/" className={classes.links}>MaterialUI</a></li>
                                <li key="210"><a href="https://github.com/reactchartjs/react-chartjs-2" className={classes.links}>react-chartjs-2</a></li>
                                <li key="220"><a href="https://webpack.js.org/" className={classes.links}>webpack</a></li>
                                <li key="230"><a href="https://babeljs.io/" className={classes.links}>babel</a></li>
                                <li key="241"><a href="https://reactrouter.com/" className={classes.links}>React router</a></li>
                            </ul>
                        </Typography>
                        <hr />
                        <Typography id="paragraph6" variant="h4" component="h1" align="center" color="textPrimary" >
                            Credits
                        </Typography>
                        <Typography variant="h5" align="left" paragraph>
                            <ul>
                                <li key="22"><a href="https://api.nbp.pl/en.html" className={classes.links}>NBP</a> for sharing currency API</li>
                                <li key="23"><a href="https://www.kaggle.com/kyanyoga/sample-sales-data/?select=sales_data_sample.csv" className={classes.links}>Kaggle</a> for sharing database sample data</li>
                            </ul>
                        </Typography>
                    </Container>
                </div>
            </main>
        </React.Fragment>


    )
}

export default Home
