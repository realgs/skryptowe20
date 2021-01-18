import React, { Component } from "react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { atomDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import README from "./About/README.md";

class AboutTab extends Component {
  constructor(props) {
    super(props);

    this.state = { md: "" };
  }

  componentWillMount() {
    fetch(README)
      .then((res) => res.text())
      .then((md) => {
        this.setState({ md });
      });
  }

  render() {
    const renderers = {
      code: ({ language, value }) => {
        return (
          <SyntaxHighlighter
            style={atomDark}
            language={language}
            children={value}
          />
        );
      },
    };
    return (
      <ReactMarkdown
        renderers={renderers}
        children={this.state.md}
        className="mt-4"
      />
    );
  }
}

export default AboutTab;
