import React, { useState, useEffect } from "react";
import HomePage from "./HomePage";

const SearchResultPage = (props) => {
  // actually we don't need this page, just go back to homepage
  alert("you searched " + props.location.searchContent);

  return (
    <HomePage />
  );
}

export default SearchResultPage;
