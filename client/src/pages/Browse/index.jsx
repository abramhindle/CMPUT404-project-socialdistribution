import { useEffect, useState } from 'react';
import AuthorPreview from '../../components/AuthorPreview';
import authorService from '../../services/author';
import './styles.css';

const Browse = () => {
  const PAGESIZE = 5;
  const [data, setData] = useState([]);
  const [pageNum, setPageNum] = useState(1);

  useEffect(() => {
    const fetchAuthors = async () => {
      try {
        const response = await authorService.getAuthors(pageNum, PAGESIZE);
        const data = response?.data;
        if (data) {
          setData(data);
        }
        console.log(data);
      } catch (e) {
        console.log(e);
      }
    };
    fetchAuthors();

  }, [pageNum]);



  const displayResults = (data) => {
    return (
      <div>
        {data?.items?.map((item) => {
          return <AuthorPreview authorData={item} key={item.id} />;
        })}
      </div>
    );
  };

  const handleNextPage = () => {
    if (data?.items?.length === PAGESIZE) {
      setPageNum(pageNum + 1);
    }
    console.log(pageNum);
  }

  const handlePrevPage = () => {
    if (pageNum > 1) {
      setPageNum(pageNum - 1);
    }
    console.log(pageNum);
  }

  return (
    <div className='authorSearchContainer'>
      <>{displayResults(data)}</>
      <div className='authorSearchButton'>
        {pageNum > 1 ? <button onClick={handlePrevPage}>Previous Page</button> : <div></div>}
        {data?.items?.length === PAGESIZE? <button onClick={handleNextPage}>Next Page</button>:<div></div>}

      </div>
    </div>
  );
};

export default Browse;
