import axios, {AxiosInstance, AxiosRequestConfig} from "axios";
import {Author, ListItem, CommentListItem, Post, Comment, Like, InboxListItem} from "..";

class API {
    private axiosInstance: AxiosInstance;
    private nodeType: "local" | "remote";
    constructor(apiURL: string, axiosConfig?: AxiosRequestConfig, nodeType:"local"|"remote" = "local") {
        this.axiosInstance = axios.create(
            {
                baseURL: apiURL,
                headers: {
                    "Content-Type": "application/json",

                },
                ...axiosConfig
            }
        );
        this.nodeType = nodeType;

    }

    public getNodeType(): "local" | "remote" {
        return this.nodeType;
    }

    public async getAuthors(page:number = 0, size:number = 25, query:string = ''):Promise<ListItem<Author>> {
        const results = await this.axiosInstance.get<Author[]>(`/authors?page=${page}&size=${size}&query=${query}`);

        return {
            type: "authors",
            items: results.data
        }
    }

    public async getAuthor(authorId:string):Promise<Author | undefined> {
        try {
            const result = await this.axiosInstance.get<Author>(`/authors/${authorId}`);
            return result.data;
        }
        catch (e) {
            return undefined;
        }
    }

    public async createAuthor(author:Author):Promise<void> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }
        await this.axiosInstance.post<void>(`/authors`, author);
    }

    public async updateAuthor(authorId:string):Promise<Author> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }
        const result = await this.axiosInstance.put<Author>(`/authors/${authorId}`);
        return result.data;
    }

    public async getFollowers(authorId:string):Promise<ListItem<Author>> {

        const results = await this.axiosInstance.get<Author[]>(`/authors/${authorId}/followers`);
        return {
            type: "authors",
            items: results.data
        }
    }

    public async addFollower(authorId: string, foreignAuthorId: string): Promise<void> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }
        return await this.axiosInstance.put<void, any>(`/authors/${authorId}/followers/${foreignAuthorId}`);
    }

    public async checkFollower(authorId:string, foreignAuthorId:string): Promise<boolean> {

        const result = await this.axiosInstance.get<boolean>(`/authors/${authorId}/followers/${foreignAuthorId}`);
        return result.data;
    }

    public async removeFollower(authorId: string, foreignAuthorId: string): Promise<void> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }
        return await this.axiosInstance.delete<void, any>(`/authors/${authorId}/followers/${foreignAuthorId}`);
    }

    public async sendFollowRequest(authorTo:Author, authorFrom:Author):Promise<void> {
        return this.axiosInstance.post(`/authors/${authorTo.id}/inbox`, {
            type: "Follow",
            summary: `${authorFrom.displayName} wants to follow you on ${authorFrom.displayName}`,
            actor: authorFrom,
            object: authorTo
        })
    }

    public async getPost(authorId:string, postId:string):Promise<Post> {
        const result = await this.axiosInstance.get<Post>(`/authors/${authorId}/posts/${postId}`);
        return result.data;
    }

    public async deletePost(authorId: string, postId: string): Promise<void> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }
        return await this.axiosInstance.delete<void, any>(`/authors/${authorId}/posts/${postId}`);
    }

    public async getPosts(authorId:string, page:number = 0, size:number = 25):Promise<ListItem<Post>> {
        const results = await this.axiosInstance.get<Post[]>(`/authors/${authorId}/posts?page=${page}&size=${size}`);
        return {
            type: "posts",
            items: results.data
        }
    }

    public async updatePost(postId: string, post: Post): Promise<Post> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }
        const result = await this.axiosInstance.put<Post>(`/authors/${post.author.id}/posts/${postId}`, post);
        return result.data;
    }

    public async createPost(authorId:string, post:Post):Promise<Post> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }
        const result = await this.axiosInstance.post<Post>(`/authors/${authorId}/posts`, post);
        return result.data;
    }

    public async getComments(authorId:string, postId: string, page:number=0, size:number=10): Promise<CommentListItem> {
        const results = await this.axiosInstance.get<CommentListItem>(`/authors/${authorId}/posts/${postId}/comments?page=${page}&size=${size}`);
        return results.data;
    }

    public async createComment(authorId:string, postId: string, comment: Comment): Promise<Comment> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }
        const result = await this.axiosInstance.post<Comment>(`/authors/${authorId}/posts/${postId}/comments`, comment);
        return result.data;
    }

    public async createLike(authorId:string, post:Post, authorFrom:Author):Promise<void> {
        return this.axiosInstance.post(`/authors/${authorId}/inbox`, {
            '@context': 'https://www.w3.org/ns/activitystreams',
            type: "Like",
            summary: `${authorFrom.displayName} likes your post`,
            author: authorFrom,
            object: post.id
        })
    }

    public async createCommentLike(authorId:string, comment:Comment, authorFrom:Author):Promise<void> {
        return this.axiosInstance.post(`/authors/${authorId}/inbox`, {
            '@context': 'https://www.w3.org/ns/activitystreams',
            type: "Like",
            summary: `${authorFrom.displayName} likes your comment`,
            author: authorFrom,
            object: comment.id
        })
    }

    public async getLiked(authorId:string):Promise<ListItem<Like>> {
        const results = await this.axiosInstance.get<Like[]>(`/authors/${authorId}/liked`);
        return {
            type: "likes",
            items: results.data
        }
    }

    public async getInbox(authorId:string):Promise<InboxListItem> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }

        const results = await this.axiosInstance.get<InboxListItem>(`/authors/${authorId}/inbox`);
        return results.data;
    }
}


export default API;