import { Parser, HtmlRenderer } from "commonmark";
import jsCookies from "js-cookies";
import { useContext, useEffect, useState } from "react";
import authorService from "../services/author";
import postService from "../services/post";
import { UserContext } from "../UserContext";
import MiniProfile from "./MiniProfile";

const Comment = ({ comment }) => {
  const { user } = useContext(UserContext);
  const [ commentState, setCommentState ] = useState(comment);

  const CMParser = new Parser({ safe: true });
  const CMWriter = new HtmlRenderer();

  useEffect(() => {
    if (comment?.id === undefined) return;
    const getCommentLikes = async () => {
      const res = await postService.getCommentLikes(comment.id.split("/").at(-5), comment.id.split("/").at(-3), comment.id.split("/").at(-1));
      console.log(res)
      setCommentState({ ...commentState, likes: res.data.items } )
    }
    getCommentLikes();
  }, [comment.id])

  const likeComment = async () => {
    try {
      const authorResponse = await authorService.getAuthor(user.author.authorID);
      await postService.likeComment(jsCookies.getItem('csrftoken'), comment.id.split("/").at(-5), { author: authorResponse.data, object: comment.id })
      setCommentState({...commentState, likes: [ ...commentState.likes, authorResponse.data]})
    } catch (e) {
      if (e.response?.status === 409) {
        alert('You have already liked this post');
      } else {
        console.log(e);
      }
    }
  }

  return (
    <div>
      { comment?.author &&
      <>
        <MiniProfile author={comment.author} />
        { comment.contentType === "text/plain" ? 
            <div className='comment'>{comment.comment}</div> 
          :
            <div
              className='comment'
              dangerouslySetInnerHTML={{
                __html: CMWriter.render(CMParser.parse(comment.comment)),
              }}
            ></div>
      }</>}
      <div className="postButton" style={{marginTop: "0"}} onClick={likeComment}>Like ({commentState?.likes?.length || 0})</div>
    </div>
  );
};

export default Comment;
