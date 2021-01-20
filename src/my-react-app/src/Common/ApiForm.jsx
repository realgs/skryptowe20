import React, { Component } from "react";
import { Form, Button } from "react-bootstrap";

class ApiForm extends Component {
  state = {
    validated: false,
  };

  handleSubmit = (event) => {
    const form = event.currentTarget;
    this.setState({ validated: form.checkValidity() });
    const from = document.getElementById("from").value;
    const to = document.getElementById("to").value;
    const currency = document.getElementById("currency").value;

    const whatToFetch = document.getElementById("type").value;

    if (whatToFetch === "currency") {
      this.props.fetchCurrency(currency, from, to);
    } else {
      this.props.fetchSales(currency, from, to);
    }

    event.stopPropagation();
    event.preventDefault();
  };

  render() {
    return (
      <React.Fragment>
        <Form
          className="mb-5"
          noValidate
          validated={this.state.validated}
          onSubmit={this.handleSubmit}
        >
          <Form.Group controlId="from" className="col-sm-6">
            <Form.Label>From</Form.Label>
            <Form.Control required type="date" />
          </Form.Group>

          <Form.Group controlId="to" className="col-sm-6">
            <Form.Label>To</Form.Label>
            <Form.Control required type="date" />
          </Form.Group>

          <Form.Group controlId="currency" className="col-sm-3">
            <Form.Label>Currency</Form.Label>
            <Form.Control required type="text" placeholder="eur, usd, gbp..." />
          </Form.Group>
          <Form.Group controlId="type" className="col-sm-3">
            <Form.Label>What should I fetch?</Form.Label>
            <Form.Control as="select" className="mr-sm-2" custom>
              <option value="currency">Currency rates</option>
              <option value="sales">Sales</option>
            </Form.Control>
          </Form.Group>
          <Button variant="primary" type="submit" className="ml-3">
            Submit
          </Button>
        </Form>
      </React.Fragment>
    );
  }
}

export default ApiForm;
