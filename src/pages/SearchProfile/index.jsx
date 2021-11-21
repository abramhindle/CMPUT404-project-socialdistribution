import React, { useState } from 'react';
import './styles.css';
import { useHistory } from 'react-router';

const SearchProfile = () => {
  const history = useHistory();
  const [ userID, setUserID ] = useState("");

  const onSubmit = () => {
    history.push(`/author/${userID}`)
  };

  return (
    <div className="searchProfileContainer">
      <input placeholder="User ID" onChange={(event) => setUserID(event.target.value)} />
      <button onClick={onSubmit}>SEARCH USER ID</button>
    </div>
  );
};

export default SearchProfile;
