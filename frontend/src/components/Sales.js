import * as React from "react";
import { Typography, Container, Link } from "@material-ui/core";
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';


const useStyles = makeStyles((theme) => ({
    contentCss: {
        backgroundColor: theme.palette.background.paper,
        padding: theme.spacing(8, 0, 6),
    }
}));


const Sales = () => {
    const classes = useStyles()

    return (
        <React.Fragment>
            <main>
                <div className={classes.contentCss}>
                    <Container maxWidth="md">
                        <Typography variant="h2" component="h1" align="center" color="textPrimary">
                            Sales API
                        </Typography>
                    </Container>
                </div>
            </main>
        </React.Fragment>


    )
}

export default Sales
