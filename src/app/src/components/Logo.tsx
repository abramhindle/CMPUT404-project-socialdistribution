import React, { useState } from 'react';
import styled from 'styled-components';

const LogoContainer = styled.div`
  text-align: center;
  height: ${window.innerHeight}px;
  font-family: Avenir Next Light;
  font-size: 200px;

  &::first-letter {
    font-size: 300px;
  }
`;

export default function Logo() {
  return <LogoContainer>Website.</LogoContainer>;
}
