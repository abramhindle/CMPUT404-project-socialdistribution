import React, { Component } from 'react'
import axios from "axios";

class UploadImage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      imagePreview: null,
      img: null,
      retrievedImage: null
    };
    this.onImageChange = this.onImageChange.bind(this);
    this.chooseFile = React.createRef();
  }

  onImageChange = event => {
    if (event.target.files && event.target.files[0]) {
      // this.state.img = event.target.files[0];
      this.setState({
        img: event.target.files[0],
        imagePreview: URL.createObjectURL(this.state.img)
      });
    }
  };
  showOpenFileDlg = () => {
    this.chooseFile.current.click()
  };

  getBase64 = (file) => {
    var reader = new FileReader();
    reader.readAsDataURL(file);
    return new Promise(resolve => {
      reader.onload = e => {
        resolve(e.target.result);
      }
    })
  };

  submitImage = () => {
    if (this.state.img != null) {
      const promises = [this.getBase64(this.state.img)]
      Promise.all(promises).then((base64) => {
        console.log(base64);
        let base64String = String(base64);// exclude "data:"
        this.postData(base64String);
      }).catch((err) => {
        console.log(err);
      });
    }
  }

  postData = async (base64String) => {
    // extract contentType from base64String
    let contentType = base64String.slice(5).split(",")[0];
    console.log(contentType);
    let data = {
      "title": "aaanother post with image",
      "source": "http://hello.com",
      "origin": "http://hh.com",
      "description": "This is an example post",
      "contentType": contentType,
      "content": base64String,
      "visibility": "PUBLIC",
      "unlisted": false
    }
    try {
      // !!!!!replace the authorID
      const response = await axios.post("service/author/c5579c15f9c24b2a80be4a1f058f9833/posts/", data);
      console.log(response.data);
    } catch (error) {
      console.log(error.message);
    }
  }

  retreivePost = async () => {
    try {
      // !!!!!replace the authorID and postID
      const response = await axios.get("service/author/c5579c15f9c24b2a80be4a1f058f9833/posts/d51cbba5-24a5-4c8d-8739-ebee69ca5a28/");
      console.log(response.data);
      let imageBase64 = response.data['content'];
      this.setState({ retrievedImage: imageBase64 });
    } catch (error) {
      console.log(error.message);
    }
  }

  render() {
    return (
      <div>
        <div>
          <img src={this.state.imagePreview} alt="imagePreview" />
          <h1>Select Image</h1>
          <button onClick={this.showOpenFileDlg}>Choose Image</button>
          <input type="file" ref={this.chooseFile} onChange={this.onImageChange} style={{ display: 'none' }}
            accept="image/png, image/jpeg" />

          <button onClick={this.submitImage}> Submit </button>
        </div>
        <div>
          <button onClick={this.retreivePost}>get image from database</button>
          <h1>Image from database</h1>
          <img src={this.state.retrievedImage} alt="retrievedImage" />
        </div>
      </div>
    )
  }
}

export default UploadImage;