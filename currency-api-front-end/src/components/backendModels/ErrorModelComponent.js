import React, {Component} from "react";


class ErrorModelComponent extends Component {

    render() {
        return (
            <React.Fragment>
                <h1>Server failed with error code: {this.props.errorCode}</h1>
                <h2>{this.props.errorMessage}</h2>
            </React.Fragment>
        );
    }

}

export default ErrorModelComponent;
