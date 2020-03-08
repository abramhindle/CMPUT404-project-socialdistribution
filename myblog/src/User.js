import React from 'react';
import 'antd/dist/antd.css';
import { List, Menu, Icon, Layout } from 'antd';
import { Button} from 'antd';
import { Input, Avatar } from 'antd';
import SimpleReactLightbox from "simple-react-lightbox";
import { SRLWrapper } from "simple-react-lightbox"; 
import './components/Header.css'
import AuthorHeader from './components/AuthorHeader'
import axios from 'axios';

//https://alligator.io/react/axios-react/

const { Header } = Layout;

const IconText = ({ type, text }) => (
  <span>
    <Button href="/posts/postid/comments" color="OldLace" icon="message" style={{width: "30px", height: "30px", backgroundColor: "white"}}></Button>
    {text}
  </span>
);


class User extends React.Component {

  state = {
    size: 'large',
    PublicPostData:[],
  };

  componentDidMount() {
    axios.get('http://localhost:8000/api/post/')
      .then(res => {
        const PublicPost = res.data;
        this.setState( {PublicPostData: PublicPost });
        console.log(this.state.PublicPostData)
      })
      .catch(function (error) {
      console.log(error);
      });
  
    
  };
  render() {
    const mystyle = {
      backgroundColor: "white",
      padding: "1%",
      color: "white",
      position: "relative",
      height: "100%",
    };

    const { Search } = Input;
  

      return(
        <view>
          <AuthorHeader/>
          <div style={mystyle}>
              <List
                  itemLayout="vertical"
                  size="large"
                  pagination={{pageSize: 5}}
                  dataSource={this.state.PublicPostData}
                  renderItem={item => (
                      <List.Item
                          key={item.title}
                          actions={[
                          <IconText type="message" text="0" key="list-vertical-message" />,
                          ]}
                          extra={
                            <SimpleReactLightbox>
                                <SRLWrapper>
                                  <img
                                    width={250}
                                    alt=""
                                    src="https://wallpaperaccess.com/full/628286.jpg"/>
                                  <img
                                  width={250}
                                  alt=""
                                  src="https://i.pinimg.com/originals/1f/53/25/1f53250c9035c9d657971712f6b38a99.jpg"/> 

                                </SRLWrapper> 
                            </SimpleReactLightbox>
                          }
                      >
                      <List.Item.Meta
                        avatar={<Avatar src={'https://cdn2.iconfinder.com/data/icons/user-icon-2-1/100/user_5-15-512.png'} />}
                        title={item.author.username}
                      />
                      {item.published}<br/><br/>
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
