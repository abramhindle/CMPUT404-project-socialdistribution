// uses setObject setter to set object to fetch response
export const setObjectFromApi = (path, setObject) => {
  fetch(path, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
      .then((corsResponse) => {
        const apiPromise = corsResponse.json();
        apiPromise.then((apiResponse) => {
          console.log(apiResponse)
          setObject(apiResponse);
        })
      })
}

// validate the token
export const validateToken = () => {
  // get a resource from the backend
  fetch("http://127.0.0.1:8000/service/authors/", {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
      .then((corsResponse) => {
        const apiPromise = corsResponse.json();
        apiPromise.then((apiResponse) => {

          // if the token is not valid
          if (apiResponse.code === 'token_not_valid') {

            // try to get a new token
            fetch("http://127.0.0.1:8000/service/api/token/refresh/", {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                'refresh': `Bearer ${localStorage.getItem('refresh')}`
              })
            })
              .then((corsResponse) => {
                const apiPromise = corsResponse.json();
                apiPromise.then((apiResponse) => {

                  // if getting a new token did not work
                  if (apiResponse.code === 'token_not_valid') {
                    // remove the token
                    localStorage.removeItem('token')
                  } else {
                    // update the token
                    localStorage.setItem('token', apiResponse.access)
                  }
                })
              })
          }
        })
      })
}
