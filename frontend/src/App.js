import React, { Component } from "react";
import Header from "./components/NavBar";
import Footer from "./components/Footer";
import CssBaseline from "@material-ui/core/CssBaseline";
import { ThemeProvider } from "@material-ui/core/styles";
import theme from "./theme.js";
import Main from "./components/Main";



class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            loaded: false,
            placeholder: "Loading"
        };
    }

    componentDidMount() {
        fetch("api/sales")
            .then(response => {
                if (response.status > 400) {
                    return this.setState(() => {
                        return { placeholder: "Something went wrong!" };
                    });
                }
                return response.json();
            })
            .then(data => {
                this.setState(() => {
                    return {
                        data,
                        loaded: true
                    };
                });
            });
    }

    render() {
        return (
            <React.StrictMode>
                <ThemeProvider theme={theme}>
                    <CssBaseline />
                    <Header /> {}
                    <div className='App'>
                        <Main />
                    </div>
                    <Footer />
                </ThemeProvider>
            </React.StrictMode>
        );
    }
}

export default App;
