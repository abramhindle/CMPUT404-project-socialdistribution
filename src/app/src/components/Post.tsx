import React from "react";
import Button, { ButtonProps } from "@mui/material/Button";
import { styled as Styled } from "@mui/material/styles";
import styled from "styled-components";

interface postItem {
  Name: String;
  ContentText: String;
  Likes: Number;
  Comments: Number;
}

const PostContainer = styled.div`
  width: 500px;
  height: 300px;
  border: 1px solid black;
  position: relative;
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
  height: "10%",
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
  height: "10%",
  padding: "3%",
  "&:hover": {
    backgroundColor: "#F9F7F5",
  },
}));

const Post: React.FC<postItem> = (props?) => {
  return (
    <PostContainer>
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
    </PostContainer>
  );
};

export default Post;
