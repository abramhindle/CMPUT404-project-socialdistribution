import './components.css';
import { useHistory } from 'react-router';
const AuthorPreview = ({ authorData }) => {
  const history = useHistory();
  const handleError = e => {
    e.target.onerror = null;
    e.target.src = 'assets/anonProfile.png';
  }

  const goToAuthor = () => {
    const authorID = authorData.id.split('/').at(-1);

    history.push(`/author/${authorID}`);
  }


  return (
    <div className='authorPreview' onClick={goToAuthor}>
      <img
        src={authorData.profileImage || 'assets/anonProfile.png'}
        alt='profile'
        onError={handleError}
      />
      <p>Name: {authorData?.displayName}</p>
      <p>Host: {authorData?.host}</p>
    </div>
  );
};

export default AuthorPreview;
