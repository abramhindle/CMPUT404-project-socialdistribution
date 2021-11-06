// uses setObject setter to set object to fetch response
export const setObjectFromApi = (path, setObject) => {
  fetch(path, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${localStorage.getItem('token')}`
      }
    })
      .then((corsResponse) => {
        const apiPromise = corsResponse.json();
        apiPromise.then((apiResponse) => {
          setObject(apiResponse);
        })
      })
}
