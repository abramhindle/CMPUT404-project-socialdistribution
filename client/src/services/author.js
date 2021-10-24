import axios from "axios";
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

const getAuthors = async (page, size) => {
  const params = new URLSearchParams(page);
  params.append(size);
  const response = await axios.get(`${baseUrl}s/`, params);
  return response;
};

const getAuthor = async (authorId) => {
  const response = await axios.get(`${baseUrl}/${authorId}`);
  return response;
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
const getInbox = async(csrfToken, authorId) => {
  const response = await axios.get(`${baseUrl}/${authorId}/inbox`);
  return response;
};

// get liked posts for author
const getLiked = async(authorId) => {
  const response = await axios.get(`${baseUrl}/${authorId}/liked`);
  return response;
};

const getFollowers = async (authorId) => {
  const response = await axios.get(`${baseUrl}/${authorId}/followers`);
  return response;
};

const follow = async (csrfToken, authorId, followerId) => {
  const response = await axios.put(`${baseUrl}/${authorId}/followers/${followerId}`,
    {},
    {
      withCredentials: true,
      headers: { "X-CSRFTOKEN": csrfToken },
      sameSite: "none"
    }
  );
  return response;
};

const authorService = {
  login,
  register,
  logout,
  getAllAuthors,
  getAuthors,
  getAuthor,
  updateAuthor,
  getLiked,
  getInbox,
  follow,
  getFollowers
};

export default authorService;