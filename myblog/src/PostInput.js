import React from 'react';
import 'antd/dist/antd.css';
import './index.css';
import { Input, Button, Switch, Select, Upload, Modal, Icon} from 'antd';

const { TextArea } = Input;
const { Option } = Select;

function handleChange(value) {
    console.log(`selected ${value}`);
}


function getBase64(file) {
return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
});
}
  

class PostInput extends React.Component {
    state = {
        previewVisible: false,
        previewImage: '',
        fileList: [
          {
            uid: '-1',
            name: 'image.png',
            status: 'done',
            url: 'https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png',
          },
          {
            uid: '-2',
            name: 'image.png',
            status: 'done',
            url: 'https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png',
          },
          {
            uid: '-3',
            name: 'image.png',
            status: 'done',
            url: 'https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png',
          },
          {
            uid: '-4',
            name: 'image.png',
            status: 'done',
            url: 'https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png',
          },
          {
            uid: '-5',
            name: 'image.png',
            status: 'error',
          },
        ],
      };

      handleCancel = () => this.setState({ previewVisible: false });

      handlePreview = async file => {
        if (!file.url && !file.preview) {
          file.preview = await getBase64(file.originFileObj);
        }
    
        this.setState({
          previewImage: file.url || file.preview,
          previewVisible: true,
        });
      };
    
      handleChange = ({ fileList }) => this.setState({ fileList });
    

    render(){
        const inputstyle = {
            backgroundColor: "white",
            padding: "1%",
            top: "40%",
            position: "relative",
            height: "20%",
      
          };

        const buttonstyle = {
            backgroundColor: "white",
            padding: "1%",
            position: "fixed",
            height: "6%",
            width: "100%",
          };

          
        const { previewVisible, previewImage, fileList } = this.state;
        const uploadButton = (
        <div>
            <Icon type="plus" />
            <div className="ant-upload-text" style={{left: "5%"}}>Upload</div>
        </div>
        );
        

        return(
            <view>
                
                <div style={inputstyle}>
                    <TextArea rows={4} />
                    <Select defaultValue="Public" style={{ width: 120, left: "93.5%"}} onChange={handleChange}>
                        <Option value="Public">Public</Option>
                        <Option value="Friends">Friends</Option>
                        <Option value="Followers">Followers</Option>
                        <Option value="Private">Private</Option>
                    </Select>

                </div>

                <div className="clearfix" style={{left: "5%"}}>
                    <Upload
                        action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
                        listType="picture-card"
                        fileList={fileList}
                        onPreview={this.handlePreview}
                        onChange={this.handleChange}
                    >
                        {fileList.length >= 8 ? null : uploadButton}
                    </Upload>
                    <Modal visible={previewVisible} footer={null} onCancel={this.handleCancel}>
                        <img alt="example" style={{ width: '100%' }} src={previewImage} />
                    </Modal>
                </div>

                <div style={buttonstyle}>
                    <Button shape="round" style={{width: "10%"} }>Post</Button>
                    <Switch style={{left: "80%"}} checkedChildren="Markdown Selected" unCheckedChildren="Markdown Unselected" />
                </div>
            </view>

        )

    }
}

export default PostInput
