import Axios from "axios";
import Author from "./models/Author";
import Comment from "./models/Comment";
import Like from "./models/Like";
import Post from "./models/Post";

const axios = Axios.create({
  baseURL: "http://localhost:3001",
});

axios.interceptors.request.use((config) => {
  config.headers = config.headers || {};
  const token = localStorage.getItem("token");
  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;
  }
  return config;
});

const api = {
  /**
   * Log into an existing author's account.
   * @returns the author
   */
  login: async (email: string, password: string): Promise<Author> => {
    const result = await axios.post("/login", { email, password });
    localStorage.setItem("token", result.data.token);
    return result.data.author;
  },

  /**
   * Register and log into a new author's account.
   * @returns the new author
   */
  register: async (
    email: string,
    password: string,
    displayName: string
  ): Promise<Author> => {
    const result = await axios.post("/register", {
      email,
      password,
      displayName,
    });
    localStorage.setItem("token", result.data.token);
    return result.data.author;
  },

  /**
   * Log out of the current author's account.
   */
  logout: () => {
    localStorage.removeItem("token");
  },

  /**
   * Actions on authors.
   */
  authors: {
    /**
     * Fetches a paginated list of all authors on the server.
     * @param page the page to return
     * @param size the number of authors per page
     * @returns a list of authors
     */
    list: async (page?: number, size?: number): Promise<Author[]> =>
      (await axios.get("/authors", { params: { page, size } })).data.items,

    /**
     * Gets data about the currently logged-in author.
     */
    getCurrent: async (): Promise<Author> =>
      (await axios.get("/authors/me")).data,

    /**
     * Actions on the author with ID `authorId`.
     */
    withId: (authorId: string) => ({
      /**
       * Fetches the profile of the author.
       * @returns profile of the author
       */
      get: async (): Promise<Author> =>
        (await axios.get(`/authors/${authorId}`)).data,

      /**
       * Updates the profile of the author.
       * @param data the new profile data of the author
       * @returns TODO
       */
      update: async (data: Author): Promise<unknown> =>
        (await axios.post(`/authors/${authorId}`, data)).data,

      /**
       * Actions relating to the author's inbox.
       */
      inbox: {
        /**
         * Fetches a paginated list of posts in the author's inbox.
         * @param page the page to return
         * @param size the number of authors per page
         * @returns a list of posts in the inbox
         */
        list: async (page?: number, size?: number): Promise<Post[]> =>
          (
            await axios.get(`/authors/${authorId}/inbox`, {
              params: { page, size },
            })
          ).data.items,

        /**
         * Send a post to the author's inbox.
         * @returns TODO
         */
        send: async (post: Post): Promise<unknown> =>
          (await axios.post(`/authors/${authorId}/inbox`, post)).data,

        /**
         * Clear the author's inbox.
         * @returns TODO
         */
        clear: async (): Promise<unknown> =>
          (await axios.delete(`/authors/${authorId}/inbox`)).data,
      },

      /**
       * Actions relating to the author's likes.
       */
      likes: {
        /**
         * Fetches a list of items the author has liked.
         */
        list: async (): Promise<(Post | Comment)[]> =>
          (await axios.get(`/authors/${authorId}/likes`)).data.items,
      },

      /**
       * Actions on the existing or potential followers of this author.
       */
      followers: {
        /**
         * Lists the followers of the author.
         * @returns a list of the profiles of the followers
         */
        list: async (): Promise<Author[]> =>
          (await axios.get(`/authors/${authorId}/followers`)).data.items,

        /**
         * Actions on the existing or potential follower with ID `followerId` of the author.
         */
        withId: (followerId: string) => ({
          /**
           * Checks if this author is in fact a follower.
           * @returns true if this author is a follower, false otherwise
           */
          isAFollower: async (): Promise<boolean> =>
            (await axios.get(`/authors/${authorId}/followers/${followerId}`))
              .data,

          /**
           * Makes this author a follower.
           * @returns TODO
           */
          follow: async (): Promise<unknown> =>
            (await axios.put(`/authors/${authorId}/followers/${followerId}`))
              .data,

          /**
           * Makes this author not a follower.
           * @returns TODO
           */
          unfollow: async (): Promise<unknown> =>
            (await axios.delete(`/authors/${authorId}/followers/${followerId}`))
              .data,
        }),
      },

      /**
       * Actions on the posts of this author.
       */
      posts: {
        /**
         * Fetches a paginated list of posts by this author.
         * @param page the page to return
         * @param size the number of posts per page
         * @returns a list of posts
         */
        list: async (page?: number, size?: number): Promise<Post[]> =>
          (
            await axios.get(`/authors/${authorId}/posts`, {
              params: { page, size },
            })
          ).data.items,

        /**
         * Creates a post with a random ID.
         * @param data the data of the post
         * @returns TODO
         */
        create: async (data: Omit<Post, "id">): Promise<unknown> =>
          (await axios.post(`/authors/${authorId}/posts`, data)).data,

        /**
         * Actions on the post with ID `postId`.
         */
        withId: (postId: string) => ({
          /**
           * Fetches the post.
           * @returns the post
           */
          get: async (): Promise<Post> =>
            (await axios.get(`/authors/${authorId}/posts/${postId}`)).data,

          /**
           * Updates the post with new data.
           * @param data the data to update the post with
           * @returns TODO
           */
          update: async (data: Post): Promise<unknown> =>
            (await axios.post(`/authors/${authorId}/posts/${postId}`, data))
              .data,

          /**
           * Creates the post.
           * @param data the data of the post
           * @returns TODO
           */
          create: async (data: Post): Promise<unknown> =>
            (await axios.put(`/authors/${authorId}/posts/${postId}`, data))
              .data,

          /**
           * Deletes the post.
           * @returns TODO
           */
          delete: async (): Promise<unknown> =>
            (await axios.delete(`/authors/${authorId}/posts/${postId}`)).data,

          /**
           * Fetches the image of this post.
           * @returns the image of this post if it exists
           */
          image: async (): Promise<Post> =>
            (await axios.get(`/authors/${authorId}/posts/${postId}/image`))
              .data,

          /**
           * Actions relating to likes on the post.
           */
          likes: {
            /**
             * List the likes on this post.
             * @returns a list of the likes on the post
             */
            list: async (): Promise<Like[]> =>
              (await axios.get(`/authors/${authorId}/posts/${postId}/likes`))
                .data.items,

            /**
             * Like the post.
             * @returns TODO
             */
            like: async (): Promise<unknown> =>
              await axios.post(
                `/authors/${authorId}/inbox`,
                (() => {
                  throw new Error("not implemented");
                })()
              ),
          },

          /**
           * Actions on the comments of this post.
           */
          comments: {
            /**
             * Gets a paginated list of comments on this post.
             * @param page the page number
             * @param size the number of comments per page
             * @returns a list of comments in the page
             */
            list: async (page?: number, size?: number): Promise<Comment[]> =>
              (
                await axios.get(
                  `/authors/${authorId}/posts/${postId}/comments`,
                  { params: { page, size } }
                )
              ).data.items,

            /**
             * Creates a comment on the post with a random ID.
             * @param data the comment data
             * @returns TODO
             */
            create: async (data: Omit<Comment, "id">): Promise<unknown> =>
              (
                await axios.post(
                  `/authors/${authorId}/posts/${postId}/comments`,
                  data
                )
              ).data,

            /**
             * Actions on the comment with ID `commentId`.
             */
            withId: (commentId: string) => ({
              /**
               * Actions relating to likes on the comment.
               */
              likes: {
                /**
                 * List the likes on this post.
                 * @returns a list of the likes on the post
                 */
                list: async (): Promise<Like[]> =>
                  (
                    await axios.get(
                      `/authors/${authorId}/posts/${postId}/comments/${commentId}/likes`
                    )
                  ).data.items,

                /**
                 * Like the post.
                 * @returns TODO
                 */
                like: async (): Promise<unknown> =>
                  await axios.post(
                    `/authors/${authorId}/inbox`,
                    (() => {
                      throw new Error("not implemented");
                    })()
                  ),
              },
            }),
          },
        }),
      },
    }),
  },
};
export default api;
