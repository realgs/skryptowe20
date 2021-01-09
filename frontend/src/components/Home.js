import * as React from "react";
import { Typography, Container, Link } from "@material-ui/core";
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';


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
    }
}));


const Home = () => {
    const classes = useStyles()

    return (
        <React.Fragment>
            <main>
                <div className={classes.heroContent}>
                    <Container maxWidth="md">
                        <Typography variant="h2" component="h1" align="center" color="textPrimary" gutterBottom>
                            REST with Django Rest Framework
                        </Typography>
                        <Typography variant="h5" align="left" paragraph>
                            <div>
                                This API offers simple GET request, fetching currency values to Polish Zloty.
                                It also allows to get sale statistics based date parameter.
                                GET requests return in form of JSON.<br />
                            </div>
                            <br />
                            <ol>
                                <li><a href="#paragraph1" className={classes.links}>Install Guide</a></li>
                                <li><a href="#paragraph2" className={classes.links}>Adding new currency</a></li>
                                <li><a href="#paragraph3" className={classes.links}>API usage</a></li>
                                <li><a href="#paragraph4" className={classes.links}>Limits</a></li>
                                <li><a href="#paragraph5" className={classes.links}>Dependencies</a></li>
                                <li><a href="#paragraph6" className={classes.links}>Credits</a></li>
                            </ol>
                        </Typography>
                        <hr />
                        <Typography id="paragraph1" variant="h4" component="h1" align="center" color="textPrimary" gutterBottom>
                            Install Guide
                        </Typography>
                        <Typography variant="h5" align="left" paragraph>
                            <div>
                                This projects implements automatic database creation for currency values.
                                It also provides sample database file sales.db for sales statistic API demonstration.
                            </div>
                            <br />
                            <ol>
                                <li><b>Clone this repo:</b><br />
                            git clone https://github.com/Rochala/skryptowe20.git</li>
                                <li><b>Install requirements</b><br />
                            pip install -r requirements.txt</li>
                                <li><b>Run initializing script</b><br />
                            python3 init.py</li>
                                <li><b>Configure Django for your needs</b></li>
                                <li><b>Start Django server</b><br />
                            python3 manage.py runserver</li>
                            </ol>
                        </Typography>
                        <hr />
                        <Typography id="paragraph2" variant="h4" component="h1" align="center" color="textPrimary" gutterBottom>
                            Adding new currency
                        </Typography>
                        <Typography variant="h5" align="left" paragraph>
                            <ol>
                                <li><b>Make sure NBP api supports it</b></li>
                                <li><b>Add new currency symbol to constants.py Currency enum</b></li>
                                <li><b>Run init.py script:</b><br />
                            python3 init.py</li>
                                <li><b>Add new variable in models.py to SalesStats class:</b></li>
                                {"{CURRENCY_SYMBOL_LOWERCASED} = models.FloatField()"}<br />
                            </ol>
                        </Typography>
                        <hr />
                        <Typography id="paragraph3" variant="h4" component="h1" align="center" color="textPrimary" gutterBottom>
                            API usage
                        </Typography>
                        <Typography variant="h5" align="left" paragraph>
                            <div>
                                {"Currency data range http://127.0.0.1:8000/CurrencyRange/?symbol={CURRENCY SYMBOL}start \
                            ={DATE START}&end={DATE END} Example usage for USD between 2020-12-01 and 2020-12-16 \
                                http://127.0.0.1:8000/CurrencyRange/?symbol=USD&start=2020-12-01&end=2020-12-16"}
                            </div>
                            <br />
                            <div>
                                {"Sales statistics http://127.0.0.1:8000/SaleStats/?date={SELECTED DATE} \
                                Example usage for fetching sales from 2005-05-17 \
                                http://127.0.0.1:8000/SaleStats/?date=2005-05-17 You can also get whole \
                                range by using http://127.0.0.1:8000/SaleStats/"}
                            </div>
                        </Typography>
                        <hr />
                        <Typography id="paragraph4" variant="h4" component="h1" align="center" color="textPrimary" gutterBottom>
                            Limits
                        </Typography>
                        <Table>
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
                        <Typography id="paragraph5" variant="h4" component="h1" align="center" color="textPrimary" gutterBottom>
                            Dependencies
                        </Typography>
                        <Typography variant="h5" align="left" paragraph>
                            <ul>
                                <li><a href="" className={classes.links}>Django</a></li>
                                <li><a href="" className={classes.links}>Django REST Framework</a></li>
                                <li><a href="" className={classes.links}>requests</a></li>
                                <li><a href="" className={classes.links}>ReactJS</a></li>
                                <li><a href="" className={classes.links}>MaterialUI</a></li>
                                <li><a href="" className={classes.links}>React router</a></li>
                            </ul>
                        </Typography>
                        <hr />
                        <Typography id="paragraph6" variant="h4" component="h1" align="center" color="textPrimary" gutterBottom>
                            Credits
                        </Typography>
                        <Typography variant="h5" align="left" paragraph>
                            <ul>
                                <li><a href="" className={classes.links}>NBP</a> for sharing currency API</li>
                                <li><a href="" className={classes.links}>Kaggle</a> for sharing database sample data</li>
                            </ul>
                        </Typography>
                    </Container>
                </div>
            </main>
        </React.Fragment>


    )
}

export default Home
