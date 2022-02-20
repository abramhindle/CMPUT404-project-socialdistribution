import React from "react";
import Button, { ButtonProps } from "@mui/material/Button";
import { styled as Styled } from "@mui/material/styles";
import styled from "styled-components";
import logo from '../logo.svg';

interface postItem {
  Name: String;
  ContentText: String;
  Likes: Number;
  Comments: Number;
  ProfilePicturePath?: String;
}

const PostContainer = styled.div`
  width: 500px;
  height: 300px;
  display: flex;
`;

const PostDetailsContainer = styled.div`
height: 100%;
width: 90%;
display: flex;
border: 1px solid black;
flex-direction: column;
position: relative;
`;

const PostProfilePictureContainer = styled.div`
height: 100%;
margin: 20px;
`;

const TopRowContainer = styled.div`
  display: flex;
  flex-direction: row;
`;

const NameContainer = styled.div`
  padding: 1%;
`;

const EditDeleteButtonContainer = styled.div`
  padding: 1%;
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  width: 100%;
`;

const ContentContainer = styled.div`
  padding: 1%;
  margin-top: 20px;
`;

const LikesCommentsContainer = styled.div`
  padding: 1%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  position: absolute;
  bottom: 0;
  left: 0;
`;

const LikesContainer = styled.div`
  padding: 1%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  width: 90px;
`;

const CommentsContainer = styled.div`
  padding: 1%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  width: 130px;
`;

const EditButton = Styled(Button)<ButtonProps>(({ theme }) => ({
  color: theme.palette.getContrastText("#e6c9a8"),
  backgroundColor: "white",
  border: "2px solid black",
  height: "90%",
  padding: "3%",
  marginRight: "10px",
  "&:hover": {
    backgroundColor: "#F9F7F5",
  },
}));

const DeleteButton = Styled(Button)<ButtonProps>(({ theme }) => ({
  color: theme.palette.getContrastText("#e6c9a8"),
  backgroundColor: "white",
  border: "2px solid black",
  height: "90%",
  padding: "3%",
  "&:hover": {
    backgroundColor: "#F9F7F5",
  },
}));

const Post: React.FC<postItem> = (props?) => {
  return (
    <PostContainer>
      <PostProfilePictureContainer>
        <img src={logo} alt="Profile" height="100" width="100" />
      </PostProfilePictureContainer>
      <PostDetailsContainer>
        <TopRowContainer>
          <NameContainer>{props?.Name}</NameContainer>
          <EditDeleteButtonContainer>
            <EditButton>Edit</EditButton>
            <DeleteButton>Delete</DeleteButton>
          </EditDeleteButtonContainer>
        </TopRowContainer>
        <ContentContainer>{props?.ContentText}</ContentContainer>
        <LikesCommentsContainer>
          <LikesContainer>{props?.Likes} Likes</LikesContainer>
          <CommentsContainer>{props?.Comments} Comments</CommentsContainer>
        </LikesCommentsContainer>
      </PostDetailsContainer>
    </PostContainer>
  );
};

export default Post;
