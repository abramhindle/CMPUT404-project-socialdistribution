import { Octokit } from '@octokit/rest';
import { useEffect, useState } from 'react';
import styled from 'styled-components';
import Activity from './Activity';

const octokit = new Octokit({
  auth: process.env.REACT_APP_GH,
  userAgent: 'Yoda',
});

const GithubContainer = styled.div`
  width: 20%;
  height: 500px;
  position: fixed;
  border: 2px solid black;
  background-color: white;
  overflow-y: scroll;
`;
const GithubHeader = styled.div`
  width: 100%;
  text-align: center;
  margin-top: 2%;
  height: 5%;
  align-items: center;
  justify-content: center;
  font-size: 150%;
  font-family: Avenir Next Light;
`;
const Github = () => {
  const [items, setItems] = useState<Array<any>>([]);
  useEffect(() => {
    async function onLoad() {
      await octokit
        .request('GET /users/{username}/events/public', {
          username: 'Sutanshu',
        })
        .then((res) => setItems(res.data))
        .catch((e) => console.log(e));
    }
    onLoad();
  }, []);

  return (
    <GithubContainer>
      <GithubHeader>Github Activity</GithubHeader>
      {items.map((item: any) => {
        return <Activity type={item?.type} payload={item?.payload} repo={item?.repo} />;
      })}
    </GithubContainer>
  );
};

export default Github;
