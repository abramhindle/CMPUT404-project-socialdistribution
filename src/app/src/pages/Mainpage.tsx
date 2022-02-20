import NavBar from "../components/NavBar";
import Post from "../components/Post";
import styled from "styled-components";

const items2 = [
  {
    Text: "Hello",
    handleClick: () => {
      console.log(1);
    },
  },
];

const HomeContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: ${window.innerHeight}px;
`;
const NavBarContainer = styled.div`
  margin-bottom: 50px;
`;

export default function Mainpage() {
  return (
    <HomeContainer>
      <NavBarContainer>
        <NavBar items={items2} />
      </NavBarContainer>

      <Post
        Name={"Seth"}
        ContentText={"Welcome to my Awesome Webiste :)"}
        Likes={10}
        Comments={6}
      />
    </HomeContainer>
  );
}
