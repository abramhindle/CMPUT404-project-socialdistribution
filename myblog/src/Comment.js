import React from 'react';
import 'antd/dist/antd.css';
import { Comment, Tooltip, List } from 'antd';
import moment from 'moment';
import { Input } from 'antd';
import { Button} from 'antd';
import './Comment.css';


const data = [
  {
    actions: [<span key="comment-list-reply-to-0">Reply to</span>],
    author: 'Commenter',
    avatar: 'https://qph.fs.quoracdn.net/main-qimg-54166a525ee4fb3097d260173688c157.webp',
    content: (
      <p>
        We supply a series of design principles, practical patterns and high quality design
        resources (Sketch and Axure), to help people create their product prototypes beautifully and
        efficiently.
      </p>
    ),
    datetime: (
      <Tooltip
        title={moment()
          .subtract(1, 'days')
          .format('YYYY-MM-DD HH:mm:ss')}
      >
        <span>
          {moment()
            .subtract(1, 'days')
            .fromNow()}
        </span>
      </Tooltip>
    ),
  },
  {
    actions: [<span key="comment-list-reply-to-0">Reply to</span>],
    author: 'Commenter',
    avatar: 'https://qph.fs.quoracdn.net/main-qimg-54166a525ee4fb3097d260173688c157.webp',
    content: (
      <p>
        We supply a series of design principles, practical patterns and high quality design
        resources (Sketch and Axure), to help people create their product prototypes beautifully and
        efficiently.
      </p>
    ),
    datetime: (
      <Tooltip
        title={moment()
          .subtract(2, 'days')
          .format('YYYY-MM-DD HH:mm:ss')}
      >
        <span>
          {moment()
            .subtract(2, 'days')
            .fromNow()}
        </span>
      </Tooltip>
    ),
  },
];

class Comments extends React.Component {
    render(){
        return(
            <view>
                <div className = "commentstyle">
                    <List
                        className="comment-list"
                        header={`${data.length} comment(s)`}
                        itemLayout="horizontal"
                        dataSource={data}
                        renderItem={item => (
                            <li>
                                <Comment
                                    actions={item.actions}
                                    author={item.author}
                                    avatar={item.avatar}
                                    content={item.content}
                                    datetime={item.datetime}
                                />
                            </li>
                        )}
                    />
                </div>

                <div className="sendstyle">
                    <Input placeholder="Enter comment here" />

                </div>
                <div className="buttonstyle" >
                  <Button shape="round">Comment</Button>

                </div>

            </view>

        )


    }

}


export default Comments;

