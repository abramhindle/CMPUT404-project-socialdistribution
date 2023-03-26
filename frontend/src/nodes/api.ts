import axios, {AxiosInstance, AxiosRequestConfig} from "axios";
import {Author, ListItem, CommentListItem, Post, Comment, Like, InboxListItem, Activity} from "..";

class API {
    private axiosInstance: AxiosInstance;
    private nodeType: "local" | "remote";
    constructor(apiURL: string, axiosConfig?: AxiosRequestConfig, nodeType:"local"|"remote" = "local") {
        this.axiosInstance = axios.create(
            {
                baseURL: apiURL,
                ...axiosConfig
            }
        );
        this.nodeType = nodeType;

    }

    public getNodeType(): "local" | "remote" {
        return this.nodeType;
    }

    public async getAuthors(page:number = 0, size:number = 25, query:string = ''):Promise<ListItem<Author>> {
        
        try {
            const results = await this.axiosInstance.get<ListItem<Author>>(`/authors/?page=${page}&size=${size}&query=${query}`);
            if (results.data.items === undefined) {
                throw new Error("items is undefined");
            }
            return results.data;
        }
        catch (e) {
            console.error(e);
            return {
                type: "authors",
                items: []
            }
        }
    }

    public async isPostLiked(postId:string, authorId:string):Promise<boolean> {
        try {
            const result = await this.axiosInstance.get<ListItem<Like>>(`/authors/${authorId}/liked`);
            const likes = result.data.items;
            for (const like of likes) {
                if (like.object.includes(postId)) {
                    return true;
                }
            }
            return false;
        }
        catch (e) {
            console.error(e);
            return false;
        }
    }

    public async isCommentLiked(commentId:string, authorId:string):Promise<boolean> {
        try {
            const result = await this.axiosInstance.get<ListItem<Like>>(`/authors/${authorId}/liked`);
            
            const likes = result.data.items;
            
            for (const like of likes) {
                
                if (like.object.includes(commentId)) {
                    return true;
                }
            }
            return false;
        }
        catch (e) {
            console.error(e);
            return false;
        }
    }

    public async getAuthor(authorId:string):Promise<Author | null> {
        try {
            const result = await this.axiosInstance.get<Author>(`/authors/${authorId}`);
            return result.data;
        }
        catch (e) {
            console.error(e);
            return null;
        }
    }

    public async createAuthor(author:Author):Promise<void> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }
        try {
            await this.axiosInstance.post<void>(`/authors/`, author);
        } catch (e) {
            console.log(e);
        }
        
    }

    public async updateAuthor(authorId:string, data:Author):Promise<Author | null> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }
        try {
            const result = await this.axiosInstance.put<Author>(`/authors/${authorId}`, data);
            return result.data;
        }
        catch (e) {
            console.error(e);
            return null;
        }
    }

    public async getFollowers(authorId:string):Promise<ListItem<Author>> {
        try {
            const results = await this.axiosInstance.get<ListItem<Author>>(`/authors/${authorId}/followers`);
            if (results.data.items === undefined) {
                throw new Error("items is undefined");
            }
            return results.data;
        }
        catch (e) {
            console.error(e);
            return {
                type: "authors",
                items: []
            }
        }
    }

    public async addFollower(authorId: string, foreignAuthorId: string): Promise<void> {
         if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
         }
        try {
        await this.axiosInstance.put<void, any>(`/authors/${authorId}/followers/${foreignAuthorId}`, {
            status:'friends'
        });
        
        let actor = await this.getAuthor(foreignAuthorId);
        let object = await this.getAuthor(authorId);
        if (actor && object) {
        await this.sendToInbox(foreignAuthorId, {
                type: 'follow',
                summary: `${object.displayName} accepted your follow request`,
                actor: actor,
                object: object
            
        });
    }
    } catch (e) {
            console.log(e);
        }
        
    }

    public async checkFollowerStatus(authorId:string, foreignAuthorId:string): Promise<string> {
        try {
            const result = await this.axiosInstance.get<string>(`/authors/${authorId}/followers/${foreignAuthorId}`);
        return result.data;
        }
        catch (e) {
            console.error(e);
            return 'not_friends'
        }
    }

    public async removeFollower(authorId: string, foreignAuthorId: string): Promise<void> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }
            try {
                console.log(authorId, foreignAuthorId)
        return await this.axiosInstance.delete<void, any>(`/authors/${authorId}/followers/${foreignAuthorId}`);
        } 
        catch (e) {
            console.log(e);
        }
        
    }

    public async sendFollowRequest(authorTo:Author, authorFrom:Author):Promise<void> {
        try {
            
            let authorId = authorTo.id.split('/').pop();
            await this.sendToInbox(authorId || '', {
                    type: 'follow',
                    summary: `${authorFrom.displayName} wants to follow you`,
                    actor: authorFrom,
                    object: authorTo
                
            })
        } catch (e) {
            console.log(e);
        }
        
    }

    public async getPost(authorId:string, postId:string):Promise<Post | null> {
        try {
            const result = await this.axiosInstance.get<Post>(`/authors/${authorId}/posts/${postId}`);
        return result.data;
        } catch (e) {
            console.error(e);
            return null;
        } 
    }

    public async deletePost(authorId: string, postId: string): Promise<void> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }

        try {
        return await this.axiosInstance.delete<void, any>(`/authors/${authorId}/posts/${postId}`);
        }
        catch (e) {
            console.log(e);
        }
    }

    public async getPosts(authorId:string, page:number = 1, size:number = 10):Promise<ListItem<Post>> {
        try {
            const results = await this.axiosInstance.get<ListItem<Post>>(`/authors/${authorId}/posts/?page=${page}&size=${size}`);
            if (results.data.items === undefined) {
                throw new Error("items is undefined");
            }
            return results.data;
        }
        catch (e) {
            console.error(e);
            return {
                type: "posts",
                items: []
            }
        }
        
    }

    public async alertNewPost(authorId:string, post:Post) {
        // Goes to everyones inbox
            let followers = await this.getFollowers(authorId);
            let followerList = followers.items;
            Promise.all(followerList.map(async follower => {
                 let followerId = follower.id.split('/').pop();
                 if (post.visibility === 'UNLISTED') {
                        return; 
                 } else if (post.visibility === 'PRIVATE') {
                        let status = await this.checkFollowerStatus(followerId || '', authorId);
                        if (status == 'true_friends') {
                            await this.sendToInbox(followerId || '',
                            post
                        )
                        }
                 } else {
                    await this.sendToInbox(followerId || '',
                    post
                )
                 }
                 

                
            }));
           
        // Add to author's inbox
        await this.sendToInbox(authorId,  post)
    }

    public async updatePost(authorId:string, postId: string, post: Post): Promise<Post> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }
        const result = await this.axiosInstance.put<Post>(`/authors/${authorId}/posts/${postId}`, post);
        return result.data;
    }

    public async createPost(authorId:string, post:Post):Promise<Post | null> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }
        try {
            
            let result = await this.axiosInstance.post<Post>(`/authors/${authorId}/posts/`, post);
            return result.data;
        }
        catch (e) {
            console.error(e);
            return null;
        }
    }

    public async getComments(authorId:string, postId: string, page:number=0, size:number=10): Promise<CommentListItem> {
        try {
            const results = await this.axiosInstance.get<CommentListItem>(`/authors/${authorId}/posts/${postId}/comments?page=${page}&size=${size}`);
            if (results.data.comments === undefined) {
                throw new Error("items is undefined");
            }
            return results.data;
        }
        catch (e) {
            console.error(e);
            return {
                type: "comments",
                page: 0,
                size: 0,
                comments: [],
                post: "",
                id: ""
            }
        }
    }

    public async createComment(authorId:string, postId: string, comment: Comment): Promise<Comment | null> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }

        try {
            const result = await this.axiosInstance.post<Comment>(`/authors/${authorId}/posts/${postId}/comments`, comment);
            await this.sendToInbox(authorId || '', comment);
            return result.data;
        }
        catch (e) {
            console.error(e);
            return null;
        }
    }

    public async createLike(authorId:string, post:Post, authorFrom:Author):Promise<void> {
        
        try {

        await this.sendToInbox(authorId, {
                "@context": "https://www.w3.org/ns/activitystreams",
                "summary": `${authorFrom.displayName} liked your post: ${post.title}`,
                type: 'like',
                author: authorFrom,
                object: post.id,
            }
        );

        } catch (e) {
            console.log(e);
        }
        
    }



    public async createCommentLike(authorId:string, comment:Comment, authorFrom:Author):Promise<void> {
      
        try {

        await this.sendToInbox(authorId, {
                    "@context": "https://www.w3.org/ns/activitystreams",
                    "summary": `${authorFrom.displayName} liked your comment`,
                    type: 'like',
                    author: authorFrom,
                    object: comment?.id || '',
                }
            );

        } catch (e) {
            console.log(e);
        }
        
    }

    public async getLiked(authorId:string):Promise<ListItem<Like>> {
        
        try {
            const results = await this.axiosInstance.get<ListItem<Like>>(`/authors/${authorId}/liked`);
        return results.data;
        } catch (e) {
            return {
                type: "likes",
                items: []
            }
        }
        
    }

    public async sendToInbox(authorId:string, activity:Activity):Promise<void> {
        const result = await this.axiosInstance.post(`/authors/${authorId}/inbox/`, activity);
        return result.data;
    }

    public async getInbox(authorId:string):Promise<InboxListItem> {
        if (this.nodeType === "remote") {
            throw new Error("Remote nodes do not support this operation");
        }
        try {
            const results = await this.axiosInstance.get<InboxListItem>(`/authors/${authorId}/inbox/`);
        return results.data;
        }
        catch (e) {
            return {
                type: "inbox",
                author: "",
                items: []
            }
        }
    }
}


export default API;