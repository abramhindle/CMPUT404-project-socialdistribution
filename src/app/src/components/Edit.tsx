import styled from 'styled-components';
import { Button, ButtonGroup, ButtonProps, SelectChangeEvent } from '@mui/material';
import { styled as Styled } from '@mui/material/styles';
import React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import FormHelperText from '@mui/material/FormHelperText';
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
  overflow-y: scroll;
  text-align: left;
  align-items: center;
`;
const Header = styled.div`
  margin-top: 1%;
  font-family: Avenir Next Light;
  font-size: 200%;
  text-align: center;
`;

const Content = styled.div`
  margin-top: 1%;
  width: 80%;
  height: 50%;
  border: 1px solid black;
  display: flex;
  flex-direction: column;
  text-align: left;
`;
const ContentType = styled.div`
  width: 80%;
  font-family: Avenir Next Light;
  font-size: 150%;
  display: flex;
  flex-direction: row;
`;

const WriteOrPreview = styled.div`
  width: 100%;
  border-bottom: 1px solid black;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
`;
const CustomButton = Styled(Button)<ButtonProps>(({ theme }) => ({
  color: theme.palette.getContrastText('#fff'),
  padding: '10px',
  backgroundColor: 'white',
  '&:hover': {
    backgroundColor: 'grey',
  },
}));
const Edit = () => {
  const [typeOfContent, setTypeOfContent] = React.useState('');
  const handleChange = (event: SelectChangeEvent) => {
    setTypeOfContent(event.target.value as string);
  };
  return (
    <EditContainer>
      <Block>
        <Header>Edit</Header>
        <ContentType>
          <FormControl fullWidth>
            <Select
              value={typeOfContent}
              onChange={handleChange}
              inputProps={{ 'aria-label': 'Without label' }}
            >
              <MenuItem value={'Normal'}>Normal</MenuItem>
              <MenuItem value={'Markdown'}>Markdown</MenuItem>
              <MenuItem value={'Latex'}>Latex</MenuItem>
            </Select>
            <FormHelperText>Type of content</FormHelperText>
          </FormControl>
        </ContentType>
        <Content>
          {' '}
          <WriteOrPreview>
            <ButtonGroup variant="text" color="inherit" size="large" sx={{ p: 1 }}>
              <CustomButton> Write </CustomButton>
              <CustomButton> Preview</CustomButton>
            </ButtonGroup>
          </WriteOrPreview>
        </Content>
      </Block>
    </EditContainer>
  );
};

export default Edit;
