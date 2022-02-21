import React from 'react';
import Button, { ButtonProps } from '@mui/material/Button';
import { styled as Styled } from '@mui/material/styles';
import styled from 'styled-components';

interface navItem {
  Text: string;
  handleClick: () => void;
}

interface NavBarProps {
  items: navItem[];
}

const NavContainer = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
  width: 100%;
  top: 0%;
  position: fixed;
  text-align: center;
  height: 5%;
  border-bottom: 1px solid;
`;

const NavItemsContainer = styled.div`
  padding: 10%;
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
`;

const ColorButton = Styled(Button)<ButtonProps>(({ theme }) => ({
  color: theme.palette.getContrastText('#e6c9a8'),
  backgroundColor: 'white',
  '&:hover': {
    backgroundColor: '#F9F7F5',
  },
}));

const NavBar: React.FC<NavBarProps> = (props) => {
  return (
    <NavContainer>
      <NavItemsContainer>
        {props?.items?.map((item: navItem) => (
          <ColorButton key={item?.Text} variant="text" onClick={() => item?.handleClick()}>
            {item?.Text}
          </ColorButton>
        ))}
      </NavItemsContainer>
    </NavContainer>
  );
};

export default NavBar;
