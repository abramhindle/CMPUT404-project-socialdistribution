import { Image } from "antd";
import ReactMarkdown from "react-markdown";
import {
  getAuthorByAuthorID,
  getRemoteAuthorByAuthorID,
} from "../requests/requestAuthor";
import { auth } from "../requests/URL";

async function getPostDataSet(postData, remote) {
  const publicPosts = [];
  for (const element of postData) {
    let contentHTML = <p>{element.content}</p>;
    if (element.contentType !== undefined) {
      const isImage =
        element.contentType.slice(0, 5) === "image" ? true : false;
      const isMarkDown =
        element.contentType.slice(5) === "markdown" ? true : false;
      if (isImage) {
        contentHTML = <Image width={150} src={element.content} />;
      } else if (isMarkDown) {
        contentHTML = <ReactMarkdown source={element.content} />;
      }
    }
    let res;
    if (remote) {
      // remote
      res = await getRemoteAuthorByAuthorID({
        URL: element.author,
        auth: auth,
      });
    } else {
      res = await getAuthorByAuthorID({ authorID: element.author });
    }
    let rawPost = element;
    rawPost["authorName"] = res.data.displayName;
    const obj = {
      title: element.title,
      content: <div style={{ margin: "24px" }}>{contentHTML}</div>,
      datetime: <span>{element.published}</span>,
      postID: element.id,
      authorName: res.data.displayName,
      github: res.data.github,
      categories: element.categories,
      rawPost: rawPost,
      remote: false,
    };
    if (remote) {
      obj.remote = true;
    }
    publicPosts.push(obj);
  }
  return publicPosts;
}

async function getFriendDataSet(friendList, remote) {
  const friendDataSet = [];
  for (const item of friendList) {
    let author;
    if (remote) {
      author = await getRemoteAuthorByAuthorID({
        URL: item,
        auth: auth,
      });
    } else {
      author = await getAuthorByAuthorID({ authorID: item });
    }
    const obj = {
      displayName: author.data.displayName,
      github: author.data.github,
      id: author.data.id,
    };
    friendDataSet.push(obj);
  }
  return friendDataSet;
}

async function getCommentDataSet(commentData, actor, remote) {
  const commentsArray = [];
  for (const comment of commentData) {
    let authorInfo;
    if (remote) {
      authorInfo = await getRemoteAuthorByAuthorID({
        URL: comment.author_id,
        auth: auth,
      });
    } else {
      authorInfo = await getAuthorByAuthorID({
        authorID: comment.author_id,
      });
    }
    const obj = {
      authorName: authorInfo.data.displayName,
      authorID: comment.author_id,
      comment: comment.comment,
      published: comment.published,
      commentid: comment.id,
      eachCommentLike: false,
      postID: comment.post_id,
      actor: actor,
    };
    commentsArray.push(obj);
  }
  return commentsArray;
}

async function getLikeDataSet(likeData, remote) {
  const likeArray = [];
  for (const like of likeData) {
    let authorInfo;
    if (remote) {
      authorInfo = await getRemoteAuthorByAuthorID({
        URL: like.author_id,
        auth: auth,
      });
    } else {
      authorInfo = await getAuthorByAuthorID({
        authorID: like.author_id,
      });
    }
    likeArray.push({
      authorName: authorInfo.data.displayName,
      authorID: like.author_id,
    });
  }
  return likeArray;
}

export { getPostDataSet, getFriendDataSet, getLikeDataSet, getCommentDataSet };
