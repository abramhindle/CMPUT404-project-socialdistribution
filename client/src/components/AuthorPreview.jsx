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

  const parseId = (fullId) => {
    return fullId ? fullId.split('/').at(-1): '';
  }


  return (
    <div className='authorPreview' onClick={goToAuthor}>
      <img
        src={authorData.profileImage || 'assets/anonProfile.png'}
        alt='profile'
        onError={handleError}
      />
      <div className='column'>
        <p className='usernameDisplay'>{authorData?.displayName}</p>
        <p className='idDisplay'>{parseId(authorData?.id)}</p>
        <p className='hostDisplay'>{authorData?.host}</p>
      </div>
    </div>
  );
};

export default AuthorPreview;
