import React from "react";
import "./components.css"
import MiniProfile from "./MiniProfile";
import { Card } from '@mui/material';

const Like = ({ like }) => {


  const muiOverride = {
    border: '1px solid #c4c4c4',
    transition: 'border 500ms ease'
  };
  return (
    <Card
      variant='outlined'
      sx = {muiOverride}
      className='itemContainer'
        >
      <MiniProfile author={like.author} /> <div className="likeText">liked your post</div>
    </Card>
  );
}

export default Like;