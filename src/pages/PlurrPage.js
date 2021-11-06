import React from 'react'
import { useUserHandler } from "../UserContext"
import { useParams } from 'react-router-dom'
import { setObjectFromApi } from "../utils"
import PlurrContainer from '../components/PlurrContainer';
import Author from './Author';
import Authors from './Authors';
import Stream from './Stream';
import Inbox from './Inbox';


export default function PlurrPage ({ page, match })  {
  const { authorId } = useParams()
  const { loggedInUser } = useUserHandler()
  const [loading, setLoading] = React.useState(true);
  const [object, setObject] = React.useState({});

  // array of page objects
  const pageObjects = [
    {
      name: "Author",
      apiRoute: `http://127.0.0.1:8000/service/author/${authorId}`,
      component: <Author author={object} />
    },
    {
      name: "Authors",
      apiRoute: `http://127.0.0.1:8000/service/authors/`,
      component: <Authors authors={object} />
    },
    {
      name: "Inbox",
      apiRoute: `http://127.0.0.1:8000/service/authors/`,
      component: <Inbox authors={object} />
    },
    {
      name: "Stream",
      apiRoute: `http://127.0.0.1:8000/service/authors/`,
      component: <Stream authors={object} />
    },
  ]

  // get page object based on page argument
  const currentPageObject = pageObjects.find(
    (pageObject) => (pageObject.name.toUpperCase() === page.toUpperCase())
  );

  // set loading to false once object has been set
  React.useEffect(() => {
    if (Object.keys(object).length !== 0) {
      setLoading(false);
      // console.log(object)
    }
  }, [object])

  // make api call and use setObject setter to set object
  React.useEffect(() => {
    if (loggedInUser.uuid !== undefined) {
      setObjectFromApi(
        currentPageObject?.apiRoute, setObject
      )
    }
  },[loggedInUser.uuid, currentPageObject.apiRoute]);
  
  // show component when loading is complete
  return (    
    <PlurrContainer>
      {loading ? null : currentPageObject?.component}
    </PlurrContainer>
  );
}
