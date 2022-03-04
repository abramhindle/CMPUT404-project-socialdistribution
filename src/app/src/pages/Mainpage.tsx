import NavBar from "../components/NavBar";
import UserPost from "../components/UserPost";
import styled from "styled-components";
import Button, { ButtonProps } from "@mui/material/Button";
import { styled as Styled } from "@mui/material/styles";
import Author from "../api/models/Author";
import Post from "../api/models/Post";
import api from "../api/api";
import { useState, useEffect } from 'react';

const items2 = [
  {
    Text: "Hello",
    handleClick: () => {
      console.log(1);
    },
  },
];

// This is for all the stuff in the Main Page
const MainPageContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: ${window.innerHeight}px;
  width: ${window.innerWidth}px;
`;

// This is for the NavBar
const NavBarContainer = styled.div`
  margin-bottom: 5%;
`;

// This is for the posts and New Post Button and Github Activity
const MainPageContentContainer = styled.div`
  display: flex;
  flex-direction: row;
  width: 100%;
`;

// This is the NewPost Button
const NewPostButton = Styled(Button)<ButtonProps>(({ theme }) => ({
  color: theme.palette.getContrastText("#e6c9a8"),
  backgroundColor: "white",
  border: "2px solid black",
  height: "10%",
  width: "90%",
  padding: "1%",
  "&:hover": {
    backgroundColor: "#F9F7F5",
  },
}));

// This holds the New Post button and Github Stream
const NewPostGithubActivityContainer = styled.div`
  width: 10%;
  display: flex;
  justify-content: column;
  margin-right: 50px;
`;

interface Props {
  currentUser?: Author;
}

export default function Mainpage({ currentUser }: Props) {
  // For now, mainpage just shows your own posts
  const [posts,setPosts]= useState<Post[]|undefined>(undefined)
  
  useEffect(() => {
    api.authors
    .withId(""+currentUser?.id)
    .posts
    .list()
    .then((data)=>setPosts(data))
    .catch((error) => {console.log(error)})
    }, [currentUser?.id,posts])

  return (
    <MainPageContainer>
      <NavBarContainer>
        <NavBar items={items2} />
      </NavBarContainer>

      <MainPageContentContainer>
        {posts?.map((post) => (
          <UserPost
              Name={"Oogway"}
              ContentText={"Po is the dragon warrior"}
              Likes={10}
              Comments={6}
              key={post.id}
            />
          ))}

        <NewPostGithubActivityContainer>
          <NewPostButton>New Post</NewPostButton>
        </NewPostGithubActivityContainer>
      </MainPageContentContainer>
    </MainPageContainer>
  );
}
