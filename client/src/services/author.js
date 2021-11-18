import axios from "axios";

const foreignURLs = ["https://plurr.herokuapp.com/service/"]
const baseUrl = "/service/author";

// register a user with credentials { username, password }
const register = async (credentials) => {
  const response = await axios.post(`${baseUrl}/register`, new URLSearchParams(credentials));
  return response;
};

const login = async (credentials) => {
  const response = await axios.post(`${baseUrl}/login`, new URLSearchParams(credentials), { withCredentials: true, sameSite: "none" });
  return response;
};

const logout = async (csrfToken) => {
  const response = await axios.post(`${baseUrl}/logout`,
    {},
    { withCredentials: true,
      headers: { "X-CSRFToken": csrfToken }});
  return response;
};

const getAllAuthors = async () => {
  const response = await axios.get(`${baseUrl}s/`);
  return response;
};

const getRemoteAuthors = async (page = 1, size = 5) => {
  const requests = []
  foreignURLs.forEach(url => {
    requests.push(axios.get(`${url}authors/?page=${page}&size=${size}`))
  });

  return await Promise.all(requests);
}

const getAuthors = async (page, size) => {
  const params = new URLSearchParams(page);
  params.append(size);
  const response = await axios.get(`${baseUrl}s/`, params);
  return response;
};

const getAuthor = async (authorId) => {
  let response;
  try {
    response = await axios.get(`${baseUrl}/${authorId}`);
  } catch {
    response = getRemoteAuthor(authorId)
  }
  return response;
};

const getRemoteAuthor = async (authorId) => {
  const requests = []
  foreignURLs.forEach(url => {
    requests.push(axios.get(`${url}author/${authorId}/`));
  });

  const responses = (await Promise.all(requests)).filter((req) => req.status === 200);
  console.log("woo")
  console.log(responses.length)
  if (responses.length !== 1) throw Error;
  else return responses[0];
};

// updates author object at given id with passed author parameter which is expected to be a
// properly formatted author
const updateAuthor = async (csrfToken, authorId, author) => {
  const response = await axios.post(`${baseUrl}/${authorId}`,
    { ...author },
    { withCredentials: true,
      headers: { "X-CSRFToken": csrfToken }});
  return response;
};

// gets inbox for author
const getInbox = async(csrfToken, authorID) => {
  const response = await axios.get(`${baseUrl}/${authorID}/inbox`,
    {
      withCredentials: true,
      headers: { "X-CSRFTOKEN": csrfToken },
      sameSite: "none"
    }
  );
  return response;
};

const clearInbox = async (csrfToken, authorID) => {
  const response = await axios.delete(`${baseUrl}/${authorID}/inbox`, 
    {
      withCredentials: true,
      headers: { "X-CSRFTOKEN": csrfToken },
      sameSite: "none"
    }
  );
  return response;
}

// get liked posts for author
const getLiked = async(authorId) => {
  const response = await axios.get(`${baseUrl}/${authorId}/liked`);
  return response;
};

const getFollowers = async (authorId) => {
  const response = await axios.get(`${baseUrl}/${authorId}/followers`);
  return response;
};

const getRemoteFollowers = async (url, authorId) => {
  const response = await axios.get(`${url}/${authorId}/followers/`);
  return response;
};

const getRemoteLiked = async (url, authorId) => {
  const response = await axios.get(`${url}/${authorId}/liked/`);
  return response;
};

const acceptFollow = async (csrfToken, authorId, foreignId) => {
  const response = await axios.put(`${baseUrl}/${authorId}/followers/${foreignId}`,
    {},
    {
      withCredentials: true,
      headers: { "X-CSRFTOKEN": csrfToken },
      sameSite: "none"
    }
  );
  return response;
};

const follow = async (csrfToken, foreignId, actor, object) => {
  const response = await axios.post(`${baseUrl}/${foreignId}/inbox`,
    { 
      type: "Follow", 
      summary: "",
      actor,
      object,
    },
    {
      withCredentials: true,
      headers: { "X-CSRFTOKEN": csrfToken },
      sameSite: "none"
    }
  );
  return response;
};

const followRemote = async (url, foreignId, actor, object) => {
  const response = await axios.post(`${url}/${foreignId}/inbox`,
    { 
      type: "Follow", 
      summary: "",
      actor,
      object,
    },
    {
      withCredentials: true,
      auth: {
        username: "lovegamer222",
        password: "hunter22"
    }}
  );
  return response;
};

const checkIsFollowing = async (authorId, followerId) => {
  const response = await axios.get(`${baseUrl}/${authorId}/followers/${followerId}`);
  return response
}

const authorService = {
  login,
  register,
  logout,
  getAllAuthors,
  getAuthors,
  acceptFollow,
  getAuthor,
  getRemoteAuthor,
  getRemoteAuthors,
  updateAuthor,
  getLiked,
  getRemoteLiked,
  getRemoteFollowers,
  getInbox,
  clearInbox,
  follow,
  followRemote,
  getFollowers,
  checkIsFollowing
};

export default authorService;