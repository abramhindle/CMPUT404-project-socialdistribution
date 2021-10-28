import React from "react";
import "./components.css"

const Like = ({ like }) => {
  return (
    <div className="itemContainer">
      { like.summary }
    </div>
  );
}

export default Like;