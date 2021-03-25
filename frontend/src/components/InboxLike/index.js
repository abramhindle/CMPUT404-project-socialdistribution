import React from "react";
import { Button, List, message, Image, Avatar } from "antd";
import { UserOutlined, CheckOutlined, CloseOutlined } from "@ant-design/icons";
import { getinboxlike } from "../../requests/requestLike";
import { getAuthorByAuthorID } from "../../requests/requestAuthor";

export default class InboxLike extends React.Component {
  constructor(props) {
    super(props);
    this._isMounted = false;
    this.state = {
      likelist: [],
      authorID: this.props.authorID,
    };
  }

  componentDidMount() {
    this._isMounted = true;
    console.log('123',this.state.authorID);
    getinboxlike({authorID : this.state.authorID}).then((res) => {
        if (res.status === 200) {
          this.setState({ likesList:res.data });
          console.log(this.state.likesList);
        }
        else {
        message.error("Fail to get likes.");
      }
    });
  }

  componentWillUnmount() {
    this._isMounted = false;
  }

//   getRequestDataSet = (requestData) => {
//     let promise = new Promise(async (resolve, reject) => {
//       const requestSet = [];
//       for (const element of requestData) {
//         const res = await getAuthorByAuthorID({ authorID: element.actor });
//         console.log("test5", element.actor);
//         requestSet.push({
//           actorName: res.data.displayName,
//           actorID: element.actor,
//         });
//       }
//       resolve(requestSet);
//     });

//     return promise;
//   };

  render() {
    const { requestDataSet } = this.state;

    return (
      <div style={{}}>
        <List
          className="likes"
          itemLayout="horizontal"
          dataSource={requestDataSet}
          renderItem={(item) => (
            <li>
              {/* <SingleRequest
                authorID={this.state.authorID}
                actorName={item.actorName}
                actorID={item.actorID}
              /> */}
            </li>
          )}
        />
      </div>
    );
  }
}