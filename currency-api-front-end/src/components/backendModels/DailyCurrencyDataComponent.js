import React, {Component} from 'react';


class DailyCurrencyDataComponent extends Component {

    render(){
        return (
            <React.Fragment>
                <h1>USD Price for date: {this.props.date}</h1>
                <h2>Price: {this.props.price}</h2>
                <h2>Interpolation: {this.props.interpolation ? 'true': 'false'}</h2>
            </React.Fragment>
        );}
}

export default DailyCurrencyDataComponent;
