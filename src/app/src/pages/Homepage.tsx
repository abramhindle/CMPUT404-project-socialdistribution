import React from 'react';
import styled from 'styled-components';
import Logo from '../components/Logo';

// const NavContainer = styled.div`
//   width: 100%;
//   top: 0%;
//   position: fixed;
//   text-align: center;
//   height: 5%;
//   border-bottom: 1px solid;
// `;

const HomepageContainer = styled.div`
  width: 100%;
  flex: display;
  align: center;
  height: 100%;
  background-color: orange;
`;
export default function Homepage() {
  return (
    <HomepageContainer>
      <Logo />
    </HomepageContainer>
  );
}
