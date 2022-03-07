import React from 'react';
import Button, { ButtonProps } from '@mui/material/Button';
import { styled as Styled } from '@mui/material/styles';
import styled from 'styled-components';
import { CloseRounded } from '@mui/icons-material';
import Backdrop from '@mui/material/Backdrop';
import Edit from './Edit';
import Author from '../api/models/Author';

interface postItem {
  Name: string;
  ContentText: string;
  Likes: Number;
  Comments: Number;
  ProfilePicturePath?: string;
  id?: any;
  currentUser: Author | undefined;
  data?: any;
}

// This is for the whole Post, which includes the profile picure, content, etc
const PostContainer = styled.div`
  width: 100%;
  height: 300px;
  display: flex;
`;

// This is for the details of post: everything except the profile picture
const PostDetailsContainer = styled.div`
  height: 100%;
  width: 90%;
  display: flex;
  border: 1px solid black;
  flex-direction: column;
  position: relative;
`;

// This is for the Profile Picture only
const PostProfilePictureContainer = styled.div`
  height: 100%;
`;

// This is for the Author name, edit button and delete button, which be at the top
const TopRowContainer = styled.div`
  display: flex;
  flex-direction: row;
`;

// This is for the author name
const NameContainer = styled.div`
  padding: 1%;
`;
// This is for the Edit and Delete buttons
const EditDeleteButtonContainer = styled.div`
  padding: 1%;
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  width: 100%;
`;

// This is for the post content, which can be text and images
const ContentContainer = styled.div`
  padding: 1%;
  margin-top: 20px;
`;

// This is for the likes and comments
const LikesCommentsContainer = styled.div`
  padding: 1%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  position: absolute;
  bottom: 0;
  left: 0;
`;

// This is for the likes
const LikesContainer = styled.div`
  padding: 1%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  width: 90px;
`;

// This is for the comments
const CommentsContainer = styled.div`
  padding: 1%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  width: 130px;
`;

const EditButton = Styled(Button)<ButtonProps>(({ theme }) => ({
  color: theme.palette.getContrastText('#e6c9a8'),
  backgroundColor: 'white',
  border: '2px solid black',
  height: '3%',
  padding: '1%',
  marginRight: '10px',
  '&:hover': {
    backgroundColor: '#F9F7F5',
  },
}));

const DeleteButton = Styled(Button)<ButtonProps>(({ theme }) => ({
  color: theme.palette.getContrastText('#e6c9a8'),
  backgroundColor: 'white',
  border: '2px solid black',
  height: '3%',
  padding: '1%',
  '&:hover': {
    backgroundColor: '#F9F7F5',
  },
}));

const UserPost: React.FC<postItem> = (props?) => {
  const [open, setOpen] = React.useState(false);

  const handleClose = () => {
    setOpen(false);
  };
  const handleToggle = () => {
    setOpen(!open);
  };

  return (
    <>
      {open ? (
        <Backdrop
          sx={{
            color: '#fff',
            zIndex: (theme) => theme.zIndex.drawer + 1,
            width: '100%',
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
          open={open}
        >
          <CloseRounded
            onClick={handleClose}
            sx={{
              '&:hover': {
                cursor: 'pointer',
              },
              marginBottom: '10px',
              borderRadius: '100%',
              border: '1px solid white',
            }}
          />
          <Edit id={props.id} currentUser={props.currentUser} data={props.data} />
        </Backdrop>
      ) : (
        <PostContainer>
          <PostProfilePictureContainer>
            <img alt="Profile" height="100" width="100" />
          </PostProfilePictureContainer>
          <PostDetailsContainer>
            <TopRowContainer>
              <NameContainer>{props?.Name}</NameContainer>
              <EditDeleteButtonContainer>
                <EditButton onClick={handleToggle}>Edit</EditButton>
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
      )}
    </>
  );
};

export default UserPost;
