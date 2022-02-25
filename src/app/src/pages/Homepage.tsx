import styled from 'styled-components';
import { styled as Styled } from '@mui/material/styles';
import Logo from '../components/Logo';
import Button, { ButtonProps } from '@mui/material/Button';
import Github from '../components/Github';

const HomeContainer = styled.div`
  display: flex;
  height: ${window.innerHeight}px;
`;

const LeftColumn = styled.div`
  height: ${window.innerHeight}px;
  width: 50%;
  background-color: #e6c9a8;
`;
const RightColumn = styled.div`
  flex: 50%;
  display: flex;
  flex-direction: column;
  height: ${window.innerHeight}px;
  font-family: Avenir Next Light;
  font-size: 200%;
  justify-content: center;
  align-items: center;
  background-color: white;
`;

const ColorButton = Styled(Button)<ButtonProps>(({ theme }) => ({
  color: theme.palette.getContrastText('#e6c9a8'),
  padding: '10px',
  marginTop: '10%',
  backgroundColor: '#e6c9a8',
  '&:hover': {
    backgroundColor: '#D4AF85',
  },
}));
export default function Homepage() {
  return (
    <HomeContainer>
      <LeftColumn>
        <Logo />
        <Github />
      </LeftColumn>
      <RightColumn>
        Welcome to a Modern Social Media Website.
        <ColorButton variant="contained">Lets get started</ColorButton>
      </RightColumn>
    </HomeContainer>
  );
}
