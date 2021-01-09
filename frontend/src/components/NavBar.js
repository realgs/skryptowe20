import * as React from "react";
import { AppBar, Toolbar, IconButton, List, ListItem, ListItemText, Container } from "@material-ui/core";
import { Home } from "@material-ui/icons";
import { makeStyles } from "@material-ui/core/styles";




const navLinks = [
    { title: 'sales', path: '/sales' },
    { title: 'currency', path: '/currency' },
]

const useStyles = makeStyles({
    navbarDisplayFlex: {
        display: 'flex',
        justifyContent: 'space-between'
    },
    navDisplayFlex: {
        display: 'flex',
        justifyContent: 'space-between'
    },
    linkText: {
        textDecoration: 'none',
        textTransform: 'uppercase',
        color: 'white'
    }
})

const Header = () => {
    const classes = useStyles();

    return (
        <AppBar position="static">
            <Toolbar>
                <Container className={classes.navbarDisplayFlex}>
                    <IconButton edge="start" color="inherit" aria-label="home">
                        <Home fontSize="large" />
                    </IconButton>
                    { /* zastapic a zmaina linka */}
                    <List component="nav" aria-labelledby="main navigation" className={classes.navDisplayFlex}>
                        {navLinks.map(({ title, path }) => (
                            <a href={path} key={title} className={classes.linkText}>
                                <ListItem button>
                                    <ListItemText primary={title} />
                                </ListItem>
                            </a>
                        ))}
                    </List>
                </Container>
            </Toolbar>
        </AppBar>
    )
}

export default Header
