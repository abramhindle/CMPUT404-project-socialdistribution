import axios from "axios";
const baseUrl = "/api/author";

const followers = async (authorId) => {
  const response = await axios.get(`${baseUrl}/${authorId}`);
  return response;
};

const follow = async (authorId, foreignId, csrfToken) => {
  const response = await axios.put(`${baseUrl}/${authorId}/${foreignId}`, {}, { withCredentials: true, "X-CSRFToken": csrfToken });
  return response;
};

const isFollowing = async (authorId, foreignId, csrfToken) => {
  const response = await axios.get(`${baseUrl}/${authorId}/${foreignId}`);
  return response;
};

const remove = async (authorId, foreignId, csrfToken) => {
  const response = await axios.delete(`${baseUrl}/${authorId}/${foreignId}`, {}, { withCredentials: true, "X-CSRFToken": csrfToken });
  return response;
}

const followService = {
  followers, follow, isFollowing, remove
};

export default followService;