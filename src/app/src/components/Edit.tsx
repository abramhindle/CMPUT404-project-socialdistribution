import styled from 'styled-components';

const EditContainer = styled.div`
  background-color: white;
  width: 80%;
  height: 80%;
`;
const Block = styled.div`
  width: 100%;
  height: 100%;
  color: black;
  display: flex;
  flex-direction: column;
  align-items: center;
`;
const Header = styled.div`
  margin-top: 1%;
  font-family: Avenir Next Light;
  font-size: 200%;
`;
const Edit = () => {
  return (
    <EditContainer>
      <Block>
        <Header>Edit</Header>
      </Block>
    </EditContainer>
  );
};

export default Edit;
