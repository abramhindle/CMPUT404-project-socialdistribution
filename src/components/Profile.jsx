import React from 'react';
import { useHistory } from 'react-router';
import githubMark from '../resources/githubMark/githubMark120px.png';
import { Button } from '@material-ui/core';

const Profile = ({ author, buttonText, onClick }) => {
  const history = useHistory();
  const sendPost = () => {
    history.push(`/submit/${author.id.split('/').at(-1)}`);
  };
  const renderProfilePicture = (
    <img src={author.profileImage || '/static/assets/anonProfile.png'} width='200' height='200' alt='profilepic' />
  );

  const renderId = <p>{author.authorID ? author.authorID : author.id.split('/').at(-1)}</p>;

  const renderHost = author.host ? (
    <div className='profileHorizontalHeader'>
      <img src='/static/assets/host.svg' height='27.5em' alt='host mark' />
      <p>&nbsp;{author.host}</p>
    </div>
  ) : (
    <></>
  );

  const renderGithub = author.github && (
    <a href={author.github}>
      <img src={githubMark} height='25em' alt='github mark' />
      <div>{author.github}</div>
    </a>
  );
  return (
    <>
      {' '}
      {author && (
        <div>
          <div className='profileHeader'>
            {renderProfilePicture}
            <div className='profileHeaderInner'>
              <h1>{author.displayName}</h1>
              {renderId}
              {renderHost}
              {renderGithub}
              <div style={{display:'flex', gap: '10px'}}>
                <Button variant='outlined' className='profileButton' onClick={onClick}>
                  {buttonText}
                </Button>
                <Button variant='outlined' className='profileButton' onClick={sendPost}>
                  Send Post
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Profile;
