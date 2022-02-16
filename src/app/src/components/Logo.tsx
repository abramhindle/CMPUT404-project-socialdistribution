import styled from 'styled-components';

const LogoContainer = styled.div`
  text-align: center;
  font-family: Avenir Next Light;
  margin-top: 40%;
  font-size: 900%;
  &::first-letter {
    color: white;
    text-shadow: 2px 2px 5px #ebb72a;
  }
`;

export default function Logo() {
  return <LogoContainer>Website.</LogoContainer>;
}
