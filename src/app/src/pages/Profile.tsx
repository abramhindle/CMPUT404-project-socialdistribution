import * as React from 'react';
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Box, IconButton, Avatar, List, Button, Typography } from '@mui/material';
import GitHubIcon from '@mui/icons-material/GitHub';
import PersonIcon from '@mui/icons-material/Person';
import NavBar from '../components/NavBar';
import Author from '../api/models/Author';
import Post from '../api/models/Post';
import UserPost from '../components/UserPost';
import api from '../api/api';

interface Props {
  currentUser?: Author;
}

export default function Profile({ currentUser }: Props): JSX.Element {
  //Get ID from params
  const { id } = useParams() as { id: string };

  //Get author from backend
  const [author, setAuthor] = useState<Author | undefined>(undefined);

  useEffect(() => {
    api.authors
      .withId(id)
      .get()
      .then((data) => setAuthor(data))
      .catch((error) => {
        console.log('No author');
      });
  }, [id]);

  //Get author's posts
  const [posts, setPosts] = useState<Post[] | undefined>(undefined);

  useEffect(() => {
    api.authors
      .withId(id)
      .posts.list(1, 5)
      .then((data) => setPosts(data))
      .catch((error) => {
        console.log(error);
      });
  }, [id, posts]);

  // If it's your profle - Edit
  let myProfile = false;
  if (currentUser && author && currentUser.id === author.id) {
    myProfile = true;
  }

  // If you follow them - Unfollow
  // You sent them a request - Request Sent
  // Else - Follow
  const [isFollowing, setFollowing] = useState(true);
  const [sentRequest, setRequestSent] = useState(false);

  const handleFollow = () => {
    setRequestSent(true);
  };

  const handleUnfollow = () => {
    setFollowing(false);
  };

  if (author !== undefined) {
    return (
      <>
        <Box sx={{ height: window.innerHeight, width: window.innerWidth }}>
          <Box style={{ height: '5%' }} sx={{ bgcolor: '#fff' }}>
            <NavBar
              items={[
                {
                  Text: '',
                  handleClick: () => {
                    console.log(1);
                  },
                },
              ]}
            />
          </Box>
          <Box style={{ display: 'flex', height: '95%' }} sx={{ bgcolor: '#fff' }}>
            <Box
              boxShadow={5}
              display="flex"
              sx={{
                flexDirection: 'column',
                width: '30%',
                justifyContent: 'center',
                alignItems: 'center',
                bgcolor: '#fff',
              }}
            >
              {author.profileImage ? null : (
                <Avatar sx={{ width: 150, height: 150, m: 2 }}>
                  <PersonIcon sx={{ width: 100, height: 100 }} />
                </Avatar>
              )}

              <Typography variant="h4" align="center">
                {author.displayName}
              </Typography>
              {author.github ? (
                <IconButton onClick={() => window.open(author.github)}>
                  <GitHubIcon />
                </IconButton>
              ) : null}

              <Box
                sx={{
                  marginBottom: 2,
                }}
              >
                <Typography variant="h6" align="center">
                  Friends: 2
                </Typography>
                <Typography variant="h6" align="center">
                  Followers: 5
                </Typography>
                <Typography variant="h6" align="center">
                  Following: 10
                </Typography>
              </Box>

              {myProfile ? (
                <Button
                  variant="contained"
                  onClick={() => {
                    alert('Clicked Edit Button');
                  }}
                >
                  Edit
                </Button>
              ) : isFollowing ? (
                <Button variant="contained" onClick={handleUnfollow}>
                  Unfollow
                </Button>
              ) : sentRequest ? (
                <Button variant="contained" disabled>
                  Request Sent
                </Button>
              ) : (
                <Button variant="contained" onClick={handleFollow}>
                  Follow
                </Button>
              )}
            </Box>

            <Box
              overflow="auto"
              display="flex"
              sx={{
                flexDirection: 'column',
                width: '70%',
                alignItems: 'center',
                mt: 0.5,
              }}
            >
              <List style={{ maxHeight: '100%', overflow: 'auto' }}>
                {posts?.map((post) => (
                  <UserPost
                    currentUser={currentUser}
                    Name={author.displayName}
                    ContentText={post.content}
                    Likes={10}
                    Comments={6}
                    key={post.id}
                    id={post.id}
                  />
                ))}
              </List>
            </Box>
          </Box>
        </Box>
      </>
    );
  }
  return <Box />;
}
