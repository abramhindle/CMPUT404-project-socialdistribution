import React from 'react';
import 'antd/dist/antd.css';
import './index.css';
import { Input, Button, Switch} from 'antd';

const { TextArea } = Input;

class PostInput extends React.Component {
   

    render(){
        const inputstyle = {
            backgroundColor: "OldLace",
            padding: "1%",
            top: "40%",
            position: "relative",
            height: "20%",
      
          };

        const buttonstyle = {
            backgroundColor: "OldLace",
            padding: "1%",
            position: "fixed",
            height: "6%",
            width: "100%",

          };
      


        return(
            <view>
                
                <div style={inputstyle}>
                    <TextArea rows={4} />
                </div>
                <div style={buttonstyle}>
                    <Button style={{width: "10%"}}>Post</Button>
                    <Switch style={{left: "80%"}} checkedChildren="Markdown Selected" unCheckedChildren="Markdown Unselected" />
                </div>
            </view>

        )

    }
}

export default PostInput
