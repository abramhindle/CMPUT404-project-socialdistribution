import Axios, { AxiosResponse } from "axios";
import Author from "./models/Author";
import Comment from "./models/Comment";
import Like from "./models/Like";
import Post from "./models/Post";

const axios = Axios.create({
  baseURL: "http://localhost:3001",
});

const api = {
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
    list: async (page?: number, size?: number) =>
      (await axios.get<Author[]>("/authors", { params: { page, size } })).data,

    /**
     * Actions on the author with ID `authorId`.
     */
    withId: (authorId: string) => ({
      /**
       * Fetches the profile of the author.
       * @returns profile of the author
       */
      get: async () => (await axios.get<Author>(`/authors/${authorId}`)).data,

      /**
       * Updates the profile of the author.
       * @param data the new profile data of the author
       * @returns TODO
       */
      update: async (data: Author) =>
        (
          await axios.post<Author, AxiosResponse<unknown>>(
            `/authors/${authorId}`,
            data
          )
        ).data,

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
        list: async (page?: number, size?: number) =>
          (
            await axios.get<Post[]>(`/authors/${authorId}/inbox`, {
              params: { page, size },
            })
          ).data,

        /**
         * Send a post to the author's inbox.
         * @returns TODO
         */
        send: async (post: Post) =>
          (
            await axios.post<Post, AxiosResponse<unknown>>(
              `/authors/${authorId}/inbox`,
              post
            )
          ).data,

        /**
         * Clear the author's inbox.
         * @returns TODO
         */
        clear: async () =>
          (await axios.delete<unknown>(`/authors/${authorId}/inbox`)).data,
      },

      /**
       * Actions relating to the author's likes.
       */
      likes: {
        /**
         * Fetches a list of items the author has liked.
         */
        list: async () =>
          (await axios.get<(Post | Comment)[]>(`/authors/${authorId}/likes`))
            .data,
      },

      /**
       * Actions on the existing or potential followers of this author.
       */
      followers: {
        /**
         * Lists the followers of the author.
         * @returns a list of the profiles of the followers
         */
        list: async () => axios.get<Author[]>(`/authors/${authorId}/followers`),

        /**
         * Actions on the existing or potential follower with ID `followerId` of the author.
         */
        withId: (followerId: string) => ({
          /**
           * Checks if this author is in fact a follower.
           * @returns true if this author is a follower, false otherwise
           */
          isAFollower: async () =>
            (
              await axios.get<boolean>(
                `/authors/${authorId}/followers/${followerId}`
              )
            ).data,

          /**
           * Makes this author a follower.
           */
          follow: async () =>
            (
              await axios.put<void, AxiosResponse<unknown>>(
                `/authors/${authorId}/followers/${followerId}`
              )
            ).data,

          /**
           * Makes this author not a follower.
           */
          unfollow: async () =>
            (
              await axios.delete<void, AxiosResponse<unknown>>(
                `/authors/${authorId}/followers/${followerId}`
              )
            ).data,
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
        list: async (page?: number, size?: number) =>
          (
            await axios.get<Post[]>(`/authors/${authorId}/posts`, {
              params: { page, size },
            })
          ).data,

        /**
         * Creates a post with a random ID.
         * @param data the data of the post
         * @returns TODO
         */
        create: async (data: Omit<Post, "id">) =>
          (
            await axios.post<Omit<Post, "id">>(
              `/authors/${authorId}/posts`,
              data
            )
          ).data,

        /**
         * Actions on the post with ID `postId`.
         */
        withId: (postId: string) => ({
          /**
           * Fetches the post.
           * @returns the post
           */
          get: async () =>
            (await axios.get<Post>(`/authors/${authorId}/posts/${postId}`))
              .data,

          /**
           * Updates the post with new data.
           * @param data the data to update the post with
           * @returns TODO
           */
          update: async (data: Post) =>
            (
              await axios.post<Post, AxiosResponse<unknown>>(
                `/authors/${authorId}/posts/${postId}`,
                data
              )
            ).data,

          /**
           * Creates the post.
           * @param data the data of the post
           * @returns TODO
           */
          create: async (data: Post) =>
            (
              await axios.put<Post, AxiosResponse<unknown>>(
                `/authors/${authorId}/posts/${postId}`,
                data
              )
            ).data,

          /**
           * Deletes the post.
           * @returns TODO
           */
          delete: async () =>
            (
              await axios.delete<void, AxiosResponse<unknown>>(
                `/authors/${authorId}/posts/${postId}`
              )
            ).data,

          /**
           * Fetches the image of this post.
           * @returns the image of this post if it exists
           */
          image: async () =>
            (
              await axios.get<Post>(
                `/authors/${authorId}/posts/${postId}/image`
              )
            ).data,

          /**
           * Actions relating to likes on the post.
           */
          likes: {
            /**
             * List the likes on this post.
             * @returns a list of the likes on the post
             */
            list: async () =>
              (
                await axios.get<Like[]>(
                  `/authors/${authorId}/posts/${postId}/likes`
                )
              ).data,

            /**
             * Like the post.
             * @returns TODO
             */
            like: async () =>
              await axios.post<Like, AxiosResponse<unknown>>(
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
            list: async (page?: number, size?: number) =>
              (
                await axios.get<Comment[]>(
                  `/authors/${authorId}/posts/${postId}/comments`,
                  { params: { page, size } }
                )
              ).data,

            /**
             * Creates a comment on the post with a random ID.
             * @param data the comment data
             * @returns TODO
             */
            create: async (data: Omit<Comment, "id">) =>
              (
                await axios.post<Omit<Comment, "id">, AxiosResponse<unknown>>(
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
                list: async () =>
                  (
                    await axios.get<Like[]>(
                      `/authors/${authorId}/posts/${postId}/comments/${commentId}/likes`
                    )
                  ).data,

                /**
                 * Like the post.
                 * @returns TODO
                 */
                like: async () =>
                  await axios.post<Like, AxiosResponse<unknown>>(
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
