import styled from 'styled-components';
import { Button, ButtonGroup, ButtonProps, SelectChangeEvent, TextField } from '@mui/material';
import { styled as Styled } from '@mui/material/styles';
import React from 'react';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import FormHelperText from '@mui/material/FormHelperText';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import remarkGfm from 'remark-gfm';
import 'katex/dist/katex.min.css';

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
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;

const ActualContent = styled.div`
  margin-top: 2%;
  width: 50%;
`;
const CustomButton = Styled(Button)<ButtonProps>(({ theme }) => ({
  color: theme.palette.getContrastText('#fff'),
  padding: '10px',
  backgroundColor: 'white',
  '&:hover': {
    backgroundColor: '#b5b5b5',
  },
}));
const Edit = () => {
  const [typeOfContent, setTypeOfContent] = React.useState('');
  const [content, setContent] = React.useState('');
  const [openWrite, setOpenWrite] = React.useState(true);

  const handleChange = (event: SelectChangeEvent) => {
    setTypeOfContent(event.target.value as string);
  };

  const handleTextChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setContent(event.target.value);
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
            <ButtonGroup
              variant="text"
              color="inherit"
              size="large"
              sx={{ p: 1, borderBottom: '1px solid black' }}
            >
              <CustomButton
                onClick={() => setOpenWrite(true)}
                sx={{ background: openWrite ? '#b5b5b5' : 'white' }}
              >
                {' '}
                Write{' '}
              </CustomButton>
              <CustomButton
                onClick={() => setOpenWrite(false)}
                sx={{ background: !openWrite ? '#b5b5b5' : 'white' }}
              >
                {' '}
                Preview
              </CustomButton>
            </ButtonGroup>
            <ActualContent>
              {openWrite ? (
                <TextField
                  id="multiline-flexible"
                  label="Content"
                  multiline
                  fullWidth
                  maxRows={10}
                  value={content}
                  onChange={handleTextChange}
                />
              ) : (
                <ReactMarkdown
                  remarkPlugins={[remarkGfm, remarkMath]}
                  rehypePlugins={[rehypeKatex]}
                  components={{
                    code({ node, inline, className, children, ...props }) {
                      const match = /language-(\w+)/.exec(className || '');
                      return !inline && match ? (
                        <SyntaxHighlighter
                          children={String(children).replace(/\n$/, '')}
                          language={match[1]}
                          PreTag="div"
                          {...props}
                        />
                      ) : (
                        <code className={className} {...props}>
                          {children}
                        </code>
                      );
                    },
                  }}
                >
                  {content}
                </ReactMarkdown>
              )}
            </ActualContent>
          </WriteOrPreview>
        </Content>
      </Block>
    </EditContainer>
  );
};

export default Edit;
