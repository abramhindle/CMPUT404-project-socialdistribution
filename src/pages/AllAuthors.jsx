import React, { Component } from 'react';
import axios from "axios";
// import {connect} from "react-redux";

class AllAuthors extends Component {

  state = {
    allAuthors: [],
  }

  componentDidMount = async () => {
    const doc = await axios.get("service/author/");
    const data = doc.data;
    console.log("all author: ", data);
    // console.log(data[0].id.split("/"));

  }

  render() {
    return (
      <div>

      </div>
    )
  }
}

export default AllAuthors;