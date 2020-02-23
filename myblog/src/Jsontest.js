import React, { Component } from 'react'
import PostData from './Posts.json'
import { List, Avatar, Button} from 'antd';
import Img from 'react-image';


const IconText = ({ type, text }) => (
    <span>
      <Button href="/posts/postid/comments" color="OldLace" icon="message" style={{width: "30px", height: "30px", backgroundColor: "OldLace"}}></Button>
      {text}
    </span>
  );

class PostList extends Component {
  
  render () {
    const mystyle = {
        backgroundColor: "OldLace",
        padding: "1%",
        color: "white",
        top: "50px",
        position: "relative",
        height: "100%",
      };
  
    return (
        <div style={mystyle}>
        <List
            itemLayout="vertical"
            size="large"
            pagination={{pageSize: 5}}
            dataSource={PostData}
            renderItem={item => (
                <List.Item
                    key={item.title}
                    actions={[
                    <IconText type="message" text="0" key="list-vertical-message" />,
                    ]}
                    extra={
                    <Img
                        width={272}
                        alt=""
                        src={item.image}/>
                    }
                >
                <List.Item.Meta
                  avatar={<Avatar src={item.avatar} />}
                  title={<a href={item.href}>{item.title}</a>}
                  description={item.description}
                />
                {item.content}
                </List.Item>
            )}
        />
    </div>

    )
  }
}

export default PostList
