import React, { Component } from "react";
import PostCard from '../posts/PostCard';
import LikeCard from './LikeCard';

// This component is used to display items in inbox
class ObjectCard extends Component {
  
  renderItem = () => {
    if (this.props.item.type === "post")  {
      return <PostCard post={this.props.item}/>
    } else if (this.props.item.type === "like") {
      return <LikeCard like={this.props.item}/>
    }
  }

  render() {
    return (
      <div>
        {this.renderItem()}
      </div>
    )
  }
}

export default ObjectCard;