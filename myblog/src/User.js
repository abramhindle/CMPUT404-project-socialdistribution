import React from 'react';
import 'antd/dist/antd.css';
import { List, Avatar, Icon } from 'antd';
import { Button} from 'antd';
import { Input } from 'antd';



const listData = [];
for (let i = 0; i < 24; i++) {
  listData.push({
    href: 'http://ant.design',
    title: `Author ${i}`,
    avatar: 'https://qph.fs.quoracdn.net/main-qimg-54166a525ee4fb3097d260173688c157.webp',
    description:
      'Icelandair',
    content:
      'Icelandair is linking to the weather forecast for the northern lights show that day providing a nice educational tip for their fans.  But they take it a step further by asking people to share their photos.',
  });
}

const IconText = ({ type, text }) => (
  <span>
    <Icon type={type} style={{ marginRight: 8 }} />
    {text}
  </span>
);


class User extends React.Component {
  state = {
    size: 'large',
  };

  
  render() {
    const mystyle = {
      backgroundColor: "OldLace",
      padding: "15px",
      color: "white",
    };

    const { size } = this.state;
    const { Search } = Input;


      return(
        <view>
          <Search placeholder="Search" />  
          <Button size={size}>My Posts</Button>
          <Button size={size}>Settings</Button>
          <Button size={size}>Logout</Button>

          <div style={mystyle}>
              <List
                  itemLayout="vertical"
                  size="large"
                  pagination={{
                  onChange: page => {
                      console.log(page);
                  },
                  pageSize: 4,
                  }}
                  dataSource={listData}
                  renderItem={item => (
                  <List.Item
                      key={item.title}
                      actions={[
                      <IconText type="message" text="2" key="list-vertical-message" />,
                      ]}
                      extra={
                      <img
                          width={272}
                          alt="logo"
                          src="https://i.pinimg.com/originals/1f/53/25/1f53250c9035c9d657971712f6b38a99.jpg"
                      />
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
        </view>

      );
    }
}


export default User;
