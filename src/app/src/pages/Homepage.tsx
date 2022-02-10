import React from 'react';
import styled from 'styled-components';
import NavBar from '../components/NavBar';

const NavContainer = styled.div`
  width: 100%;
  position: absolute;
  text-align: center;
  height: 5%;
  border-bottom: 1px solid;
`;

const HomepageContainer = styled.div`
  width: 100%;
  flex: display;
  align: center;
`;
export default function Homepage() {
  return (
    <HomepageContainer>
      <NavContainer>
        <NavBar />
      </NavContainer>
      <div>Hello homepage!</div>
    </HomepageContainer>
  );
}
