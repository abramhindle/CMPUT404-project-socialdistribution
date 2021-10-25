import React, { useEffect, useState } from "react";
import { useParams } from "react-router";
import Post from "../../components/Post";
import Comment from "../../components/Comment";
import postService from "../../services/post";
import jsCookies from "js-cookies";
import { Parser, HtmlRenderer } from "commonmark";
import "./styles.css"

const ViewPost = () => {
  const CMParser = new Parser();
  const CMWriter = new HtmlRenderer();
  const { authorID, postID } = useParams();
  const [ comments, setComments ] = useState([]);
  const [ comment, setComment ] = useState("");
  const [ commentType, setCommentType ] = useState("Text")
  const [ post, setPost ] = useState([]);

  useEffect(() => {
    const getPost = async () => {
      const response = await postService.getPost(jsCookies.getItem("csrftoken") , authorID, postID);
      const likeRes = await postService.getLikes(authorID, postID);
      setPost({ ...response.data, likes: likeRes.data.items });
    };

    const getComments = async () => {
      const response = await postService.getComments(jsCookies.getItem("csrftoken"), authorID, postID, 1, 5);
      console.log("Comments")
      console.log(response)
      setComments(response.data.comments.map(async (comment) => {
        const likeRes = await postService.getCommentLikes(authorID, postID, comment.id.split('/').at(-1))
        return { ...comment, likes: likeRes.data.items }
      }));
    };  

    getPost();
    getComments();
  }, [ authorID, postID ]);

  const submitComment = async () => {
    const response = await postService.createComment(jsCookies.getItem("csrftoken"), authorID, postID, { commentType, comment });
    console.log(response);
    setComments(...comments, { ...response.data })
  };

  return (
    <div>
      <div className="myPostContainer">
        <Post post={post} />
      </div>
      <div className="myPostContainer">
        { comments && comments.map((comment) => <Comment comment={comment} />)}

        <select onChange={(e) => setCommentType(e.target.value === "Text" ? "text/plain" : "text/markdown")}>
          <option>Text</option>
          <option>Markdown</option>
        </select>
        <input onChange={(e) => setComment(e.target.value) } />
        <div>
          <p>Preview</p>
          { commentType === "text/plain" ? 
              <div className='cmPreview'>{comment}</div> 
            :
              <div
                className='cmPreview'
                dangerouslySetInnerHTML={{
                  __html: CMWriter.render(CMParser.parse(comment)),
                }}
              ></div>
          }
        </div>
        <br/>
        <button onClick={submitComment}>Submit Comment</button>
      </div>
    </div>  
  );
}

export default ViewPost;