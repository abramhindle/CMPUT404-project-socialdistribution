import React from "react";

class ErrorBoundary extends React.Component {
  constructor() {
    super();
    this.state = {
      hasError: false,
    }
  }

  static getDerivedStateFromError(error) {
    // handling exception
    console.log("Error (From <func>getDerivedStateFromError):", error);
    return { hasError: true }
  }

  componentDidCatch(err, info) {
    /*
    * err: content of the error
    * info: component which throws the error
    */
    console.log(err, info);
  }

  render() {
    if (this.state.hasError) {
      return <div>Something went wrong</div> // show this page when error occurs
    }

    return this.props.children;
  }
}

export default ErrorBoundary;