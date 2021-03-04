import React, { Component } from "react";
import "../../styles/likeCard.css";

// This component is used to display the like
class LikeCard extends Component {
  render() {
    return (
      <div id='like-object' style={{ border: "solid 1px grey" }}>
        {this.props.like.summary}
      </div>
    )
  }
}

export default LikeCard;