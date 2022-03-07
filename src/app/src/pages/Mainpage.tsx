import NavBar from '../components/NavBar';
import UserPost from '../components/UserPost';
import styled from 'styled-components';
import Author from '../api/models/Author';
import Post from '../api/models/Post';
import api from '../api/api';
import Add from '../components/Add';
import { useState, useEffect } from 'react';
import Backdrop from '@mui/material/Backdrop';
import { CloseRounded } from '@mui/icons-material';
import Fab from '@mui/material/Fab';
import AddIcon from '@mui/icons-material/Add';

const items2 = [
  {
    Text: 'Logout',
    handleClick: () => {
      localStorage.removeItem('token');
      window?.location?.reload();
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

// // This is the NewPost Button
// const NewPostButton = Styled(Button)<ButtonProps>(({ theme }) => ({
//   color: theme.palette.getContrastText('#e6c9a8'),
//   backgroundColor: 'white',
//   border: '2px solid black',
//   height: '10%',
//   width: '90%',
//   padding: '1%',
//   '&:hover': {
//     backgroundColor: '#F9F7F5',
//   },
// }));

// // This holds the New Post button and Github Stream
// const NewPostGithubActivityContainer = styled.div`
//   width: 10%;
//   display: flex;
//   justify-content: column;
//   margin-right: 50px;
// `;

interface Props {
  currentUser?: Author;
}

export default function Mainpage({ currentUser }: Props) {
  // For now, mainpage just shows your own posts
  const [posts, setPosts] = useState<Post[] | undefined>(undefined);
  const [open, setOpen] = useState(false);

  const handleClose = () => {
    setOpen(false);
  };
  const handleToggle = () => {
    setOpen(!open);
  };

  useEffect(() => {
    api.authors
      .withId('' + currentUser?.id)
      .posts.list(1, 5)
      .then((data) => {
        setPosts(data);
      })
      .catch((error) => {});
  }, [currentUser?.id, posts]);

  return (
    <MainPageContainer>
      <NavBarContainer>
        <NavBar items={items2} />
      </NavBarContainer>
      <Fab
        color="primary"
        aria-label="check"
        sx={{ color: 'black', background: '#46ECA6', '&:hover': { background: '#18E78F' } }}
      >
        <AddIcon onClick={handleToggle} />
      </Fab>
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
          <Add currentUser={currentUser} />
        </Backdrop>
      ) : (
        <MainPageContentContainer>
          {posts?.map((post) => (
            <UserPost
              data={post}
              Name={'' + currentUser?.displayName}
              currentUser={currentUser}
              ContentText={post.content}
              Likes={10}
              Comments={6}
              key={post.id}
              id={post.id}
            />
          ))}
        </MainPageContentContainer>
      )}
    </MainPageContainer>
  );
}
